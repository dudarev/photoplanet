// http://stackoverflow.com/questions/6288931/how-to-implement-the-vote-up-and-down-function-like-stack-overflow
jQuery(function($) {

    $("a.vote").on('click', voteClick);

    function voteClick(event) {
        var voteLink, item;

        voteLink = $(this);
        photo = voteLink.closest('.photo');
        photo_id = photo.attr('data-photoid');

        $.ajax({
            url: '/photo/' + photo_id + '/vote',
            data: {vote_type: voteLink.text()},
            type: 'POST',
            success: function(data){
                voteLink.siblings('.vote_count').text(data.vote_count);
            },
            error:   function(data){alert('Some error occured');}
        });
    }

});
