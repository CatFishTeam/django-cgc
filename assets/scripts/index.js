import Cookies from 'js-cookie'

$('#createDeck .single-card').click( function() {

    postData(`/deck-add-card`, {answer: 42})
        .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
        .catch(error => console.error(error));

    //TODO
    if($(this).find('.single-card__number').text() > 0) {
        $(this).find('.single-card__number').text($(this).find('.single-card__number').text() - 1);
    }

    /*
    //TODO On validate: check card disponibility within back
    //Tableau deck -> Add card to deck + add visual
    deck = []
    deck.forEach( (e) => {
        Object(e)
        //if clicked is in e

    });

    $('.deck div').each( function() {
        if($(this).text() == $card.data('name')) {
            console.log('Coucou');
        } else {
            $('.deck').append("<div>" + $card.data('name') + "</div>");
        }
    });
    */

    function addToDeck(card) {
        //TODO : Check if card is already present
        //

    }
    //console.log($(e.target).find('.single-card__number').html())
});


function postData(url = ``, data = {}) {
    // Default options are marked with *
    return fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            'X-CSRF-TOKEN': Cookies.get('csrftoken')
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
        .then(response => response.json()); // parses response to JSON
}
