#coding: utf-8

# setting static
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder')

#ajax form jquery.form
$('#id').ajaxForm(function (responseText, responseXML) {});
