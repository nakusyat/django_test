from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.views.generic import View
from subprocess import call

import forms
import filehandler
import os
import webbrowser


class IndexView(View):

    template_name = "smt/index.html"
    form_uploader = forms.UploadTextFileForm
    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
    public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
    files_dir = os.path.join(public_dir, 'files/')
    raw_dir = os.path.join(public_dir, 'raw/')
    extensions = ['.txt']

    def dispatch(self, request, *args, **kwargs):
        form_uploader = self.form_uploader()

        if 'upload' in request.POST:
            form = self.form_uploader(request.POST, request.FILES)
            if form.is_valid():
                temp_file = request.FILES['file']
                filehandler.move_temp_file(temp_file, self.files_dir)


        files = filehandler.get_uploaded_files_by_extension(self.extensions[:], self.files_dir)

        return render_to_response(self.template_name,
            {
                'form': form_uploader,
                'files': files,
                'test':'index'
            }, RequestContext(request))


class Plain2SntView(View):

    template_name = 'smt/plain2snt.html'
    plain2snt_dir = os.path.join(IndexView.public_dir, 'plain2snt/')
    extensions = ['.vcb', '.snt']

    def dispatch(self, request, *args, **kwargs):
        
        plain2snt_files = filehandler.get_uploaded_files_by_extension(self.extensions[:], self.plain2snt_dir)
        
        return render_to_response(self.template_name,
            {
                'plain2snt_files': plain2snt_files,
                'test':'index'
            }, RequestContext(request))


class TokenizeView(View):

    template_name = 'smt/tokenize.html'
    form_ibm_models = forms.IBMModelOptions
    tokenized_dir = os.path.join(IndexView.public_dir, 'tokenized/')

    def dispatch(self, request, *args, **kwargs):
        form_models = self.form_ibm_models()
        if request.POST:
            filehandler.process_files(request.POST.getlist('files'), IndexView.files_dir, self.tokenized_dir)
        tokenized_files = filehandler.get_uploaded_files_by_extension(IndexView.extensions[:], self.tokenized_dir)

        return render_to_response(self.template_name,
            {
                'tokenized_files': tokenized_files,
                'form_models': form_models,
                'test':'index'
            }, RequestContext(request))


class WordClassesCoocView(View):

    template_name = 'smt/word_classes.html'
    wordcl_cooc_dir = os.path.join(IndexView.public_dir, 'wordcl/')
    extensions = ['.classes', '.cats', '.cooc']

    def dispatch(self, request, *args, **kwargs):
        wc_files = filehandler.get_uploaded_files_by_extension(self.extensions[:], self.wordcl_cooc_dir)

        return render_to_response(self.template_name,
                {
                    'wc_files': wc_files,
                    'test':'index'
                }, RequestContext(request))


class TextAlignView(View):

    template_name = 'smt/aligned.html'
    aligned_dir = os.path.join(IndexView.public_dir, 'aligned/')
    extensions = ['.final', '.config', '.gizacfg', '.perp', '.vcb']
    spl_src = ''
    spl_trg = ''
    source_voc = ''
    target_voc = ''

    def dispatch(self, request, *args, **kwargs):
        if request.POST:
            form = TokenizeView.form_ibm_models(request.POST)
            if form.is_valid():
                models = form.cleaned_data["models"]
                source_file = request.POST.get('source', 0)
                target_file = request.POST.get('target', 0)

                if 'align' in request.POST:
                    if source_file and target_file:
                        self.init_properties(source_file, target_file)
                        models = self.get_ibm_model_list(models)
                        self.process_alignment(source_file, target_file, models)
        aligned_files = filehandler.get_uploaded_files_by_extension(self.extensions[:], self.aligned_dir)

        return render_to_response(self.template_name,
            {
                'aligned_files': aligned_files,
                'test':'index'
            }, RequestContext(request))

    def init_properties(self, source_file, target_file):
        self.spl_src = source_file.split(".", 1)[0]
        self.spl_trg = target_file.split(".", 1)[0]
        self.source_voc = self.spl_src + '.vcb'
        self.target_voc = self.spl_trg + '.vcb'

    def process_alignment(self, source_file, target_file, models):
        call(["public/giza/bin/plain2snt.out", TokenizeView.tokenized_dir + source_file, TokenizeView.tokenized_dir + target_file])
        call(["public/giza/bin/mkcls", '-p' + TokenizeView.tokenized_dir + source_file, '-V' + TokenizeView.tokenized_dir + source_file + '.vcb.classes'])
        call(["public/giza/bin/mkcls", '-p' + TokenizeView.tokenized_dir + target_file, '-V' + TokenizeView.tokenized_dir + target_file + '.vcb.classes'])

        filehandler.move_files_in_extensions(Plain2SntView.extensions[:], TokenizeView.tokenized_dir, Plain2SntView.plain2snt_dir )

        with open(Plain2SntView.plain2snt_dir + self.spl_src + '_' + self.spl_trg + '.cooc', "w+") as output:
            call(["public/giza/bin/snt2cooc.out", Plain2SntView.plain2snt_dir + self.source_voc, Plain2SntView.plain2snt_dir + self.target_voc, Plain2SntView.plain2snt_dir + self.spl_src + '_' + self.spl_trg + '.snt'], stdout = output)

        extensions = ['.classes', '.cats']
        filehandler.move_files_in_extensions(extensions[:], TokenizeView.tokenized_dir, WordClassesCoocView.wordcl_cooc_dir )

        extensions = ['.cooc']
        filehandler.move_files_in_extensions(extensions[:], Plain2SntView.plain2snt_dir, WordClassesCoocView.wordcl_cooc_dir )

        call(["public/giza/bin/GIZA++", '-S', Plain2SntView.plain2snt_dir + self.source_voc, '-T', Plain2SntView.plain2snt_dir + self.target_voc, '-C', Plain2SntView.plain2snt_dir + self.spl_src + '_' + self.spl_trg + '.snt', '-cooc', WordClassesCoocView.wordcl_cooc_dir + self.spl_src + '_' + self.spl_trg + '.cooc', '-mh', '0'] + models)

        filehandler.move_files_in_extensions(self.extensions[:], IndexView.main_dir, self.aligned_dir)

    def get_ibm_model_list(self, models):
        models_list = []
        for key, model in models.iteritems():
            models_list.append('-model'+ str(key) + 'iterations ' + str(model))
        models_list.append('-o')
        models_list.append(self.spl_src + 'ibm3')
        return models_list


class OpenFileView(View):
    url_namespace = 'smt:home'

    def dispatch(self, request, *args, **kwargs):
        file_name = kwargs['file_name']

        if os.path.isfile(TokenizeView.tokenized_dir + file_name):
            webbrowser.open(TokenizeView.tokenized_dir + file_name)
            self.url_namespace = 'smt:tokenize'
        elif os.path.isfile(WordClassesCoocView.wordcl_cooc_dir + file_name):
            webbrowser.open(WordClassesCoocView.wordcl_cooc_dir + file_name)
            self.url_namespace = 'smt:wc'
        elif os.path.isfile(Plain2SntView.plain2snt_dir + file_name):
            webbrowser.open(Plain2SntView.plain2snt_dir + file_name)
            self.url_namespace = 'smt:vcb'
        elif os.path.isfile(TextAlignView.aligned_dir + file_name):
            webbrowser.open(TextAlignView.aligned_dir + file_name)
            self.url_namespace = 'smt:align'
        elif os.path.isfile(IndexView.files_dir + file_name):
            webbrowser.open(IndexView.files_dir + file_name)

        return redirect(reverse(self.url_namespace))


class DeleteFileView(View):
    url_namespace = 'smt:home'

    def dispatch(self, request, *args, **kwargs):
        file_name = kwargs['file_name']

        if os.path.isfile(TokenizeView.tokenized_dir + file_name):
            os.remove(TokenizeView.tokenized_dir + file_name)
            self.url_namespace = 'smt:tokenize'
        elif os.path.isfile(IndexView.files_dir + file_name):
            os.remove(IndexView.files_dir + file_name)
        elif os.path.isfile(Plain2SntView.plain2snt_dir + file_name):
            os.remove(Plain2SntView.plain2snt_dir + file_name)
            self.url_namespace = 'smt:vcb'
        elif os.path.isfile(TextAlignView.aligned_dir + file_name):
            os.remove(TextAlignView.aligned_dir + file_name)
            self.url_namespace = 'smt:align'
        elif os.path.isfile(WordClassesCoocView.wordcl_cooc_dir + file_name):
            os.remove(WordClassesCoocView.wordcl_cooc_dir + file_name)
            self.url_namespace = 'smt:wc'

        return redirect(reverse(self.url_namespace))
