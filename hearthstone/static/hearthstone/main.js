$('#createDeck .single-card').click( function() {
    //TODO
    if($(this).find('.single-card__number').text() > 0) {
        $(this).find('.single-card__number').text($(this).find('.single-card__number').text() - 1);
    }

    $card = $(this)

    $('.deck').append("<div>" + $card.data('name') + "</div>");
    $('.deck div').each( function() {
        if($(this).text() == $card.data('name')) {
            console.log('Coucou');
        } else {
            $('.deck').append("<div>" + $card.data('name') + "</div>");
        }
    });
    //console.log($(e.target).find('.single-card__number').html())
});
