import Cookies from 'js-cookie'

let deck = []; //Tuple {"id": cardId, "count": number}

$('#createDeck .single-card').click( function() {
    decreaseCard($(this));
});

function addToDeck(card) {
    const cardId = card.data('id');
    if(deck.length > 0) {
        deck.forEach( (e) => {
            if(e['id'] === cardId){
                e['count'] += 1;
                throw BreakException;
            } else {
                deck.push({'id': cardId, 'count': 1})
            }
        })
    } else {
        deck.push({'id': cardId, 'count': 1})
    }
    console.log(deck)
}

function decreaseCard(card) {
    let quantity = card.find('.single-card__number').text();
    if( quantity > 0) {
        quantity -= 1
        card.find('.single-card__number').text( quantity );
        if (quantity == 0){
            card.css('opacity', 0.4)
        }
        addToDeck(card)
    }
}

$('#save-deck').click( () => {
    postData(`/save-deck`, {title: $('#deck-title').val(), deck: deck})
        .then(data => console.log(JSON.stringify(data)))
        .catch(error => console.error(error))
        .then(() => {
            //window.location = "/my-decks"
    })
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
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
        .then(response => response.json()); // parses response to JSON
}
