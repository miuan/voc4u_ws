function setup()
{
	jQuery.support.cors = true;
	params = {};
	$.get('template/template.html',params, function(data)
	{
		var content = $('#content_data').html();
		$('body').html( data );
		$('#content').html(content);
		addStyleSheed("style/designer.css");
		if ($.browser.msie && $.browser.version.substr(0,1)<7) {
			addStyleSheed("style/designer_ie6.css");
		}
	}, "text");


function addBackgroundCss()
{
	
}

function addStyleSheed(file)
{
	if (document.createStyleSheet)
	{
	    document.createStyleSheet(file);
	}
	else
	{
			$('head').append('<link rel="stylesheet" href="'+file+'" type="text/css" />');
	}
		
	}
}