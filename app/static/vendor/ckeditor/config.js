/**
 * @license Copyright (c) 2003-2020, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.mathJaxLib = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_HTML';
	
	config.extraPlugins = 'lineutils';
	config.extraPlugins = 'dialog';
	config.extraPlugins = 'clipboard';

	config.extraPlugins = 'widget';

	config.extraPlugins = 'dialogui';
	config.extraPlugins = 'fakeobjects';
	
	config.extraPlugins = 'link';
		
	config.extraPlugins = 'youtube';

	config.extraPlugins = 'codesnippet';
	
};
