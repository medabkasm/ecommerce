


$('submit').submit(function(e){
$.post('home:users_posts', $(this).serialize(), function(data){
alert('get the search ');
$('.container .row .posts').html(data);
});
e.preventDefault();
});
