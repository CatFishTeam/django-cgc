import Cookies from 'js-cookie'
import * as Toastr from "toastr";

let deck = []; //{"id": cardId, "count": number}

$('#createDeck .single-card').click( function() {
    decreaseCard($(this));
});

function addToDeck(card) {
    const cardId = card.data('id');
    const cardName = card.data('name');
    let exit = false;
    deck.forEach( (e) => { //use some()
        if(e['id'] === cardId){
            e['count'] += 1;
            exit = true;
        }
    });
    if(exit) return;
    deck.push({'id': cardId, 'count': 1, 'name': cardName});
}

function decreaseCard(card) {
    let quantity = card.find('.single-card__number').text();
    if( quantity > 0) {
        quantity -= 1;
        card.find('.single-card__number').text( quantity );
        if (quantity == 0){
            card.css('opacity', 0.4)
        }
        addToDeck(card)
        displayDeck()
    }
}

function displayDeck() {
    $('.deck__container').empty();
    deck.forEach((e)=> {
        console.log(e)
        $('.deck__container').append('<div class="deck__card" data-id="' + e.id + '">' + e.name + '<span>x' + e.count + '</span></div>')
    })
}

$('body').on('click', '.deck__card', function() {
    removeFromDeck($(this).data('id'))
});

function removeFromDeck(cardId){
    let exit = false;
    deck.forEach( (e) => {
        if(e['id'] === cardId){
            if(e['count'] > 1) {
                e['count'] -= 1;
            } else {
                var filteredItems = this.items.filter(function (e) {
                    return e !== item;
                });
            }
        }
    });
    if(exit) return;
    deck.push({'id': cardId, 'count': 1, 'name': cardName});
    console.log(deck)
}

let link2Deck
$('#save-deck').click( () => {
    postData(`/save-deck`, {title: $('#deck__title').val(), deck: deck})
        .then(data => link2Deck = '/show-deck/' + JSON.stringify(data))
        .catch(error => console.error(error))
        .then(() => {
            Toastr.success('<a href="'+link2Deck+'">Consulter son deck</a>','Deck créé avec succès',)
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
