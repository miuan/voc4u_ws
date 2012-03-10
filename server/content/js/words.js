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
	//hideAllDetail(false);

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
			//$('#feedback').html(data);
			//$('body').append(data);
				    alert("Data Loaded: " + getScriptPath());
			});
}

function showWords(data) 
{
	var htmltemp = '<div class="word">\
		<div class="word_row" onClick="javascript:showDetail('+ "'{id}'" + ');">' +
			'<h2>{learn} <span class="native_head" id="native_head_{id}">{native_head}</span></h2></div>' +
					'<div class="native_details" id="native_details_{id}">{native_details}</div>' +
			"</div>";
	var htmldetail = '<div class="native_detail">\
			<span class="native_detail_vote_up" onClick="javascript:voteDetail(' + "'{detail_id}'" +')">(+)</span>\
				{native_detail}\
			<span class="native_detail_vote_down" onClick="javascript:voteDetailDown(' + "'{detail_id}'" +')">(-)</span>\
			</div>';
	var htmlheadnatives = 
		'<span class="native_detail" id="native_{id}">\
			{natives}\
		</span>';
	var htmlnative = '<span class="native_detail_native">\
			<a href="#" onClick="javascript:voteEditWord(' + "'{detail_id}', '{native}'" +')">{native}</a>\
		</span>';
	var htmldesc = 
		'<span class="native_detail_desc">\
			<a href="#" onClick="javascript:voteEditDesc(' + "'{detail_id}', '{native_detail_desc}'" +')">{desc}</a>\
		</span>';
	var htmlpronouc = ' <span class="pronouc">[{pronouc}]</span>';
	var htmlspec = ' <span class="spec">({spec})</span>';
	var htmlout = "" + data.len;
	
	var ID = 0;
	
	for(var i in data.data)
	{
		word = data.data[i].word;
		//htmlout += '<div><h2>' + word.learn + '</h2>';
		
		var learn = word.learn;
		
		if(word.pronouc != null && word.pronouc.length > 0)
			learn += htmlpronouc.replace("{pronouc}", word.pronouc);
		if(word.spec != null && word.spec.length > 0)
			learn += htmlspec.replace("{spec}", word.spec);
		
		
		//htmlout += htmltemp;
				
		natives = word.natives;
		var native_details = "";
		var native_head = "";
		for(var k in natives)
		{
			native = natives[k];
			var nativedesc = htmlnative
				.replace(/{native}/g, native.native);//htmldetailnative.replace(/{native_detail}/g, native.native);
			
			
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
	$('#words').html(htmlout);
	alert(htmlout);
	
	
	$("div.word_row").mouseover(function() {
		$(this).addClass("word_row_selected")
	}).mouseout(function() {
		$(this).removeClass("word_row_selected");
	});

//	$("div").click(
//			function() {
//				var color = $(this).css("background-color");
//				$("#result").html(
//						"That div is <span style='color:" + color + ";'>"
//								+ color + "</span>.");
//			});
	
	hideAllDetail(true);
}

function showWordsOld(data) {
	$('#words').html(data);

	$("div.word_row").mouseover(function() {
		$(this).addClass("word_row_selected")
	}).mouseout(function() {
		$(this).removeClass("word_row_selected");
	});

//	$("div").click(
//			function() {
//				var color = $(this).css("background-color");
//				$("#result").html(
//						"That div is <span style='color:" + color + ";'>"
//								+ color + "</span>.");
//			});
	
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
	data = 
	{ 
			m: form.m.value,
			l: form.l.value,
			n: form.n.value,
			lc: form.lc.value,
			nc: form.nc.value
	};
	
	addWordCustomParam(data, form, "lp");
	addWordCustomParam(data, form, "ld");
	addWordCustomParam(data, form, "ls");
	addWordCustomParam(data, form, "np");
	addWordCustomParam(data, form, "nd");
	addWordCustomParam(data, form, "ns");
	
	$.get("/wordctrl", data,
		function(data)
		{
		//$('#feedback').html(data);
		$('#feedback').text(data);
		//$('body').append(data);
			   //  alert("Data Loaded: " + data);
		});
	
	
}