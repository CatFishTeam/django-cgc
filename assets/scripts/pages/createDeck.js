let deck = []; //Tuple {cardId: number}
$('#createDeck .single-card').click( function() {
    decreaseCard($(this));
});

/*
postData(`/deck-add-card`, {answer: 42})
    .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
    .catch(error => console.error(error));

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
*/

function addToDeck(card) {
    cardId = card.data('id');
    if(deck.length > 0) {
        console.log(cardId);
        deck.forEach( (e) => {
            if( Object.keys(e)[0] = cardId ) {
                deck[e] += 1
            } else {
                deck.push({cardId: 1})
            }
            console.log(deck)
        })
    } else {
        deck.push({cardId: 1})
    }

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
