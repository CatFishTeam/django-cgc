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
    countCard();
}

function countCard(){
    let countCard = 0;
    deck.forEach((e) => {
        countCard += e['count'];
    });
    $('.card__count-number').text(countCard)
    return countCard
}

function decreaseCard(card) {
    let quantity = card.find('.single-card__number').text();
    if( quantity > 0) {
        quantity -= 1;
        card.find('.single-card__number').text( quantity );
        if (quantity == 0){
            card.css('opacity', 0.4)
        }
        addToDeck(card);
        displayDeck()
    }
}

function displayDeck() {
    $('.deck__container').empty();
    deck.forEach((e)=> {
        $('.deck__container').append('<div class="deck__card" data-id="' + e.id + '">' + e.name + '<span>x' + e.count + '</span></div>')
    })
}

$('body').on('click', '.deck__card', function() {
    removeFromDeck($(this).data('id'))
});

function removeFromDeck(cardId){
    deck.forEach( (e) => {
        if(e['id'] === cardId){
            if(e['count'] > 1) {
                e['count'] -= 1;
            } else {
                let filteredDeck = deck.filter( i => {
                    return i !== e;
                });
                deck = filteredDeck;
            }
        }
    });
    $('.single-card').each( function() {
        if($(this).data('id') === cardId){
            if($(this).find('.single-card__number').text() === "0"){
                console.log($(this))
                $(this).css('opacity', 1)
            }
            $(this).find('.single-card__number').text( parseInt($(this).find('.single-card__number').text()) + 1)
        }
    });
    countCard();
    displayDeck();
}

let link2Deck;
$('#save-deck').click( () => {
    let failed = false
    if(countCard() !== 30) {
        Toastr.warning("Votre deck doit comporter 30 cartes !");
        failed = true
    }
    if( $("#deck__title").val().length < 3) {
        Toastr.warning("Votre deck doit être nommé");
        failed = true
    }
    if(failed) return;
    postData(`/save-deck`, {title: $('#deck__title').val(), deck: deck})
        .then(data => link2Deck = '/show-deck/' + JSON.stringify(data))
        .catch(error => console.error(error))
        .then(() => {
            Toastr.success('<a href="'+link2Deck+'">Consulter son deck &rarr;</a>','Deck créé avec succès',)
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
