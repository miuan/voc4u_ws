//var SERVER = "http://voc4u9.appspot.com"
var SERVER = "http://localhost:9999"

function wordVote(id) {

}

function hideAllDetail(fast) {

	$("div.word").removeClass("word_bordered");
	if (!fast) {
		$("span.native_head").show(100);
		$("div.native_details").hide(100);
	}
	else
	{
		$("span.native_head").show();
		$("div.native_details").hide();
	}
		

}

function showDetail(id) {
	// hideAllDetail(false);

	idall = "#word_detail_" + id;
	obj = $(idall);
	obj.addClass("word_bordered");

	iddetail = '#native_details_' + id;
	idnative = '#native_head_' + id;
	var v = $(iddetail);
	if(v.css('display') == 'none')
	{ 
		   v.slideDown('fast'); 
		   $(idnative).fadeToggle(400);
	} 
	else { 
		  v.hide('fast'); 
		  $(idnative).fadeToggle(400);
		}
	

	
	

}

function voteDetail(wordid)
{
	data = 
	{ 
			m: 'vote',
			id: wordid
	};
	$.get("/wordctrl", data,
			function(data)
			{
			// $('#feedback').html(data);
			// $('body').append(data);
				    alert("Data Loaded: " + getScriptPath());
			}, "text");
}

function showWords(data) 
{
	
	var htmltemp = '<div class="word">\
		<div class="word_row" onClick="javascript:showDetail('+ "'{id}'" + ');">' +
			'<h2>{learn} <span class="native_head" id="native_head_{id}">{native_head}</span></h2></div>' +
					'<div class="native_details" id="native_details_{id}">{native_details}</div>' +
			"</div>";
	var htmldetail = '<div class="native_detail">\
				{native_detail}\
			</div>';
	var htmlheadnatives = 
		'<span class="native_detail" id="native_{id}">\
			{natives}\
		</span>';
	var htmlnative = '<span class="native_detail_native">\
			<span onClick="javascript:voteEditWord(' + "'{detail_id}', '{native}'" +')">{native}</span>\
		</span>';
	var htmldesc = 
		'<span class="native_detail_desc">\
			<a href="#" onClick="javascript:voteEditDesc(' + "'{detail_id}', '{native_detail_desc}'" +')">{desc}</a>\
		</span>';
	var htmlpronouc = ' <span class="pronouc">[{pronouc}]</span>';
	var htmlspec = ' <span class="spec">({spec})</span>';
	var htmlout = "";
	
	var ID = 0;
	
	for(var i in data.data)
	{
		word = data.data[i].word;
		// htmlout += '<div><h2>' + word.learn + '</h2>';
		
		var learn = word.learn;
		
		if(word.pronouc != null && word.pronouc.length > 0)
			learn += htmlpronouc.replace("{pronouc}", word.pronouc);
		if(word.spec != null && word.spec.length > 0)
			learn += htmlspec.replace("{spec}", word.spec);
		
		
		// htmlout += htmltemp;
				
		natives = word.natives;
		var native_details = "";
		var native_head = "";
		for(var k in natives)
		{
			native = natives[k];
			var nativedesc = htmlnative
				.replace(/{native}/g, native.native);// htmldetailnative.replace(/{native_detail}/g,
														// native.native);
			
			
			if(native_head.length > 0)
			{
				native_head += ", ";
			}
			
			native_head += native.native;
			
			
			if(native.desc != null && native.desc.length > 0)
			{
				nativedesc += htmldesc.replace("{desc}", native.desc);
			}
			
			
			native_details += htmldetail
								.replace(/{native_detail}/g, nativedesc)
								.replace(/{detail_id}/g, native.id);
		}
		
		htmlout += htmltemp.replace("{learn}", learn)
						.replace("{native_details}", native_details)
						.replace("{native_head}", native_head)
						.replace(/{id}/g, ID++);
		
	}
	
	if(htmlout.length > 0)
	{
		$('#words').html(htmlout);
		
	}
	else
	{
		$('#words').html('<div id="empty"><div id="inner">' + $('#words_empty').html() + '</div></div>');
	}
	
	
	
	
	$("div.word_row").mouseover(function() {
		$(this).addClass("word_row_selected")
	}).mouseout(function() {
		$(this).removeClass("word_row_selected");
	});

// $("div").click(
// function() {
// var color = $(this).css("background-color");
// $("#result").html(
// "That div is <span style='color:" + color + ";'>"
// + color + "</span>.");
// });
	
	hideAllDetail(true);
}

function showWordsOld(data) {
	$('#words').html(data);

	$("div.word_row").mouseover(function() {
		$(this).addClass("word_row_selected")
	}).mouseout(function() {
		$(this).removeClass("word_row_selected");
	});

// $("div").click(
// function() {
// var color = $(this).css("background-color");
// $("#result").html(
// "That div is <span style='color:" + color + ";'>"
// + color + "</span>.");
// });
	
	hideAllDetail(true);
}

function showWordsddss(id, words) {

	$(id).html("ahoj draci" + words.len + words.words.length);

	var items = [];
	var arr = [];

	$.each(words.words, function(key, val) {
		if (arr[val.learn] == null) {
			arr[val.learn] = val.native;
		} else {
			prev = arr[val.learn];
			arr[val.learn] = prev + ", " + val.native;
		}

	});

	$.each(arr, function(key, val) {
		items.push('<li id="' + 1 + '">' + "dsf" + '</li>');
	});

	$('<ul/>', {
		'class' : 'my-new-list',
		html : arr.join('')
	}).appendTo('body');
}

function addWordCustomParam(data, form, key)
{
	if(form[key].value != "")
	{
		data[key] = form[key].value;
	}
}

function addWord(form)
{
	data = $('#form_add_word').serialize();
// {
// m: form.m.value,
// l: form.l.value,
// n: form.n.value,
// lc: form.lc.value,
// nc: form.nc.value
// };
	
	lv = $('#form_add_word_l').val();
	nv = $('#form_add_word_n').val();
	
	if(lv.length < 1 || nv.length < 1)
	{
		alert("learn and native must be filled!");
		return;
	}
	
// addWordCustomParam(data, form, "lp");
// addWordCustomParam(data, form, "ld");
// addWordCustomParam(data, form, "ls");
// addWordCustomParam(data, form, "np");
// addWordCustomParam(data, form, "nd");
// addWordCustomParam(data, form, "ns");
	$('#add_word_button').hide(); 
	$('#add_word_progress').show();
	
	var addr = SERVER + "/wordctrl"; 
	
	$.get(addr, data,
		function(data)
		{
		feedback = $('#words_w');
		if(feedback.length > 0)
		{
			//feedback.text(data);
		}
		else
		{
			window.location = "vocabulary.html"
		}
		
		$('#navigate_group_latest').click();
		$('#add_word_progress').hide();
		$('#add_word_button').show();
		
		// $('body').append(data);
			   // alert("Data Loaded: " + data);
		});
	
	
}


function addLanguageSelector(where, type)
{
	var types = [
	             	{
	             		code:"CZ",
	             		flag:"http://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/800px-Flag_of_the_Czech_Republic.svg.png"
	             	},
	            	{
	             		code:"EN",
	             		flag:"http://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg/800px-Flag_of_the_United_Kingdom_%283-5%29.svg.png"
	            	},
	            	{
	            		code:"DE",
	            		flag: "http://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Flag_of_Germany.svg/800px-Flag_of_Germany.svg.png"
	            	}, 
	            	{
	            		code:"FR",
	            		flag:"http://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_France.svg"
	            	},
	            	{
	            		code:"IT",
	            		flag:"http://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Flag_of_Italy.svg/800px-Flag_of_Italy.svg.png"
	            	}, 
	            	{
	            		code:"SP",
	            			flag:"http://upload.wikimedia.org/wikipedia/commons/b/b1/Flag_of_the_Spain_Under_Franco.png"
	            	}, 
	            	{
	            		code:"KR",
	            		flag: "http://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/800px-Flag_of_South_Korea.svg.png"
	            	}, 
	            	{
	            		code:"PL",
	            		flag:"http://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Flag_of_Poland.svg/800px-Flag_of_Poland.svg.png"
	            	}, 
	            	{
	            		code:"PT",
	            		flag: "http://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_Portugal.svg/600px-Flag_of_Portugal.svg.png"
	            	}, 
	            	{
	            		code:"RU",
	            		flag: "http://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Russia.svg/800px-Flag_of_Russia.svg.png"
	            	}];
	             
	var flags = [
	             // "http://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/800px-Flag_of_the_United_States.svg.png",
	             
	             "http://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Russia.svg/800px-Flag_of_Russia.svg.png",
	             
	             "http://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_Norway.svg/800px-Flag_of_Norway.svg.png",
	             
	             "http://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/800px-Flag_of_the_People%27s_Republic_of_China.svg.png",
	             "http://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/800px-Flag_of_South_Korea.svg.png",
	             "http://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Turkey.svg/800px-Flag_of_Turkey.svg.png",
	             
	             "http://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/800px-Flag_of_India.svg.png",
	             "http://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Flag_of_Saudi_Arabia.svg/750px-Flag_of_Saudi_Arabia.svg.png"];
var id = where + type;
	
	var htmlout = "";
	var obj = $(id);
	var groupid = 'add_word_form_button_'+type;
	for(var t in types)
	{
		var m = types[t].code;
		var flag = types[t].flag;
		var newid = groupid + '_' + m;
		var a = '<div id="'+newid+'" onClick="javascript:set' + type + '(' + "'" + m + "');" + '"></div>';
		obj.append(a);
		created = $('#' + newid);
		created.append('<div>' + m + '</div>');
		created.append('<img src="' + flag + '"/>');
		
		
		created.addClass(groupid);
		// class="add_word_form_button_'+type+'";
		
		// htmlout += a;
	}
	
	// $(id).html(htmlout)
}

function showAddWordForm()
{
	params = {};
	$.get('template/vocabulary_form.html',params, function(data)
	{
		$('#vocabulary_form').html(data);
		addLanguageSelector("#add_word_form_", "learn");
		addLanguageSelector("#add_word_form_", "native");
if (document.createStyleSheet)
{
    document.createStyleSheet("style/add_word.css");
}
else
{
		$('head').append('<link rel="stylesheet" href="style/add_word.css" type="text/css" />');
}
		
		setnative('CZ');
		setlearn('EN');
	}, "text");
}

function highlingSelected(id, selected, noSelected)
{
	oldSelect = $("."+ selected);
	oldSelect.removeClass(selected);
	oldSelect.addClass(noSelected);
	
	link = $(id);
	link.removeClass(noSelected);
	link.addClass(selected); 
}

var lselect = 0;
var nselect = 0;
var __page = 0;
var __groups = [0, 7, 14];

function setnative(id, code, otherid)
{
	if(nselect != id)
	{
		var type = "native";
		$(".add_word_form_button_" + type).removeClass("add_word_form_button_select");
		link = $("#add_word_form_button_" + type + "_"+ id);
		link.addClass("add_word_form_button_select"); 
	
	
	var prev = nselect;
	nselect = id;
	if(nselect == lselect)
	{
		
		setlearn(prev)
	}
	$('#form_add_word_nc').val(nselect);
	updateWords();
	
	}

}

function setlearn(id, code, otherid)
{
	if(lselect != id)
	{
		var type = "learn";
		$(".add_word_form_button_" + type).removeClass("add_word_form_button_select");
		link = $("#add_word_form_button_" + type + "_"+ id);
		link.addClass("add_word_form_button_select"); 
	
	
	var prev = lselect;
	lselect = id;
	if(nselect == lselect)
	{
		setnative(prev)
	}
	$('#form_add_word_lc').val(lselect);
		updateWords();
	}
}


var updateTimer = 0;
function updateWords()
{
	$('#words').addClass('loading');
	// .html('<img src="img/loader.gif"/>');
	if(updateTimer != 0)
	{
		clearTimeout(updateTimer);
	}
	
	updateTimer = setTimeout("updateWordsCore()",2000);
}

function updateWordsCoreDone(data)
{
	showWords(data);
	$('#words').removeClass('loading');
// showWords('#words', data);
// $('body').append(data);
	   //alert("Data Loaded: " + data);	
}

function updateWordsCore()
{
	data = 
	{ 
			m: "show",
			lc: lselect,
			nc: nselect,
			t: "json",
			p:__page
	};
	
	var addr = SERVER + "/wordctrl"; 
	
	$.getJSON(addr, data,
	// $.getJSON("template/test.html",
			function(data2)
			{
			
			updateWordsCoreDone(data2);
				
			});
//$.get(SERVER + "/wordctrl", data,
//function(data)
//			{
//alert("Data Loaded: " + data);
//});
}


function changeGroup(group)
{
	changePage(__groups[group]);
}

function selectGroupByPage(page)
{
	var grp;
	for(var i = __groups.length -1;i > -1; i--)
	{
		grp = __groups[i];
		if(grp <= page)
		{
			var id = '#navigate_group_' + i;
			$('#navigate_groups span').removeClass('selected_group');
			$(id).addClass('selected_group');
			
			break;
		}
	}
	
}

function changeGroupLatest()
{
	
	
}

function changePage(page)
{
	__page = page;
	
	if(__page > -1)
	{
		selectGroupByPage(page);
		var id = '#words_navigate_' + page;
		$('#words_navigate span').removeClass('selected_group');
		$(id).addClass('selected_group');
		$('#words_navigate').show();
	}
	else
	{
		$('#navigate_groups span').removeClass('selected_group');
		$('#navigate_group_latest').addClass('selected_group');
		$('#words_navigate').hide();
	}
	updateWords();
}

function prepareWordsWindow()
{
// $('#navigate_group_1').bind('click', function(){changePage(20);});
// $('#navigate_group_2').click(function(){
// changePage(20);
// });
// $('#navigate_group_3').click(changePage(90));
	var navigate = $('#words_navigate');
	for(var i = 0; i != 21; i++)
	{
		var id = "words_navigate_" + i;
		var func ="javascript:changePage(" + i + ");"
		navigate.append('<span id="'+id+'" onClick="'+func+'">'+ i + "</span>");
		$("#"+id).click(function(){
			changePage(i);
		});
	}
}