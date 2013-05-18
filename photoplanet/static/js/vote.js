// http://stackoverflow.com/questions/6288931/how-to-implement-the-vote-up-and-down-function-like-stack-overflow
jQuery(function($) {

    $("a.vote").on('click', voteClick);

    function voteClick(event) {
        var voteLink, item;

        voteLink = $(this);
        photo = voteLink.closest('.photo');
        photo_id = photo.attr('data-photoid');

        console.log('photo id:');
        console.log(voteLink.text());
        console.log();

        $.ajax({
            url: '/photo/' + photo_id + '/vote',
            data: {vote_type: voteLink.text()},
            type: 'POST',
            success: function(data){alert(JSON.stringify(data));},
            error:   function(data){alert('Some error occured');}
        });
    }

});
