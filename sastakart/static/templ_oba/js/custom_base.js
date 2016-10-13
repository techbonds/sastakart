$(document).ready(function(){
 
if($('#homepage_yes').length > 0)
{  
    $("#skart_img_link").attr('href','javascript:void(0);');
    $("#home_link").attr('href','javascript:void(0);');
    $("#skart_img_link_nm").attr('href','javascript:void(0);');
    $("#home_link_nm").attr('href','javascript:void(0);');
    
}

// alert($('#id_searchbar').val());

$('a').on('click', function(event) {

    if (!event.ctrlKey && !event.shiftKey && !event.metaKey && event.which != 2){



$('#reviews_tab a').click(function (e) {
   e.preventDefault()
   $(this).tab('show')
});



if($('#homepage_yes').length > 0)
{ 
   if(this.id != "skart_img_link_nm" && this.id != "home_link_nm" && this.id != "elec_drop" && this.id != "fash_drop" && this.id != "fb_footer"
     && this.id != "instagram_footer" && this.id != "twitter_footer" && this.id != "gplus_footer" && this.id != "email_footer" && this.href !="javascript:void(0);") 
  {$('html').css('overflow', 'hidden');  
  $('#loading_yolo').show(100); $('#top_level_div').fadeTo(0, 0.2);}
}
else
{
    if(this.id != "elec_drop" && this.id != "fash_drop" && this.id != "ama_reviews"
     && this.id != "flip_reviews" && this.id != "snap_reviews" && this.id != "pay_reviews" && this.href !="javascript:void(0);" && this.id != "fb_footer"
     && this.id != "instagram_footer" && this.id != "twitter_footer" && this.id != "gplus_footer" && this.id != "email_footer" && this.id != "faq1"
      && this.id != "faq2" && this.id != "faq3") 
  {$('html').css('overflow', 'hidden');  
  $('#loading_yolo').show(100); $('#top_level_div').fadeTo(0, 0.2);}
}


if(this.id != "skart_img_link" && this.id != "home_link" && this.id != "elec_drop" && this.id != "fash_drop" && 
    this.id != "skart_img_link_nm" && this.id != "home_link_nm" && this.id != "ama_reviews"
     && this.id != "flip_reviews" && this.id != "snap_reviews" && this.id != "pay_reviews" && this.href !="javascript:void(0);" && this.id != "fb_footer"
     && this.id != "instagram_footer" && this.id != "twitter_footer" && this.id != "gplus_footer" && this.id != "email_footer" && this.id != "faq1"
      && this.id != "faq2" && this.id != "faq3")
    {
    var url = this.href;
     $("*").find("a").each(function(){
        if(this.href != url)
    {this.href="javascript:void(0);";}
});

     $(document).bind('touchmove', function(e) {
    e.preventDefault();

});

$('html').css('overflow', 'hidden');

$("*").find("input").each(function(){
        $(this).prop('disabled',true);
});

$("*").find("button").each(function(){
        $(this).prop('disabled',true);
});
}


$('#elec_cat').on('click', 'a', function() {
    
    $('#loading_yolo').show(100); $('#top_level_div').fadeTo(0, 0.2);
    
    });

$('#fash_cat').on('click', 'a', function() {
    
    $('#loading_yolo').show(100); $('#top_level_div').fadeTo(0, 0.2);
   
    });

$('#elec_cat_nm').on('click', 'a', function() {
    
    $('#loading_yolo').show(100); $('#top_level_div').fadeTo(0, 0.2);
    
    });

$('#fash_cat_nm').on('click', 'a', function() {
    
    $('#loading_yolo').show(100); $('#top_level_div').fadeTo(0, 0.2);
   
    });
}
});

    $('a').each(function(){
        this.href = this.href.replace('dummy', this.text.toLowerCase().replace(/ /g,'-'));
    });
    if($('#id_searchbar').val().length == 0)
    {
        $('#id_searchbut').prop('disabled',true);
       
    }


    if($('#id_searchbar_mob').val().length == 0)
    {
        
        $('#id_searchbut_mob').prop('disabled',true);
    }


    $('#id_searchbar').keyup(function(){
        $('#id_searchbut').prop('disabled', this.value == "" ? true : false); 
       
    });

$('#id_searchbar').on('blur',function(){
       
        $('#id_searchbut').prop('disabled', this.value == "" ? true : false); 
    });

$('#id_searchbar_mob').on('blur',function(){
        
        $('#id_searchbut_mob').prop('disabled', this.value == "" ? true : false); 
    });



 $('#id_searchbar_mob').keyup(function(){
    
        $('#id_searchbut_mob').prop('disabled', this.value == "" ? true : false);    
    });
  

$('#id_searchbut').click(function(event){
    if (!event.ctrlKey && !event.shiftKey && !event.metaKey && event.which != 2){
        $('#loading_yolo').show(100); $('#top_level_div').fadeTo(0, 0.2);
        $('html').css('overflow', 'hidden');
    var url = this.href;
     $("#top_level_div").find("a").each(function(){
       this.href="javascript:void(0);";
});}
});




$('#id_searchbut_mob').click(function(){
    $(document).bind('touchmove', function(e) {
    e.preventDefault();
});
    
$("#top_level_div").find("a").each(function(){
    this.href="javascript:void(0);";
});
});




});


