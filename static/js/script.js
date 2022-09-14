

async function view(id)
{
    var url = `http://192.168.1.8:5000/movie?id=${id}`;
    try
    {
        var response = await fetch(url);
        var data = await response.json();
        



        if(data)
        {
            var headDIV = document.getElementById("detailheader");

            var div = document.getElementById("results");
            div.innerHTML = "";
            headDIV.innerHTML = `
            <h2>${data[0].movie_name}</h2>
            <h3>${data[0].theatre_name}</h3>
            <p><strong>Date : </strong>${data[0].date_} <strong>Time : </strong> ${data[0].time} <strong> Flight Name: </strong> ${data[0].name}</p>
            `

            headDIV.style.display = "block";

            for(var i = 0; i < data.length; i++)
            {

                var template = `<div class="card mb-3" style="max-width: 540px;">
                <div class="row no-gutters">
                  <div class="col-md-4">
                    <img src="static/img/ticket.jpg" class="card-img" alt="...">
                  </div>
                  <div class="col-md-8">
                    <div class="card-body">
                      <h5 class="card-title">User : ${data[i].booking_name}</h5>
                      <p class="card-text">
                      <strong>Tickets: </strong>${data[i].tickets} <br>
                      <strong>Price: </strong>Rs.${data[i].price} <br>
                      </p>
                    </div>
                  </div>
                </div>
              </div>`
                div.innerHTML += template;
            }
        }
    }
    catch(error)
    {
        console.log(error);
    }
}

function create_my_account_divs(data)
{
    var div = document.getElementById("account_container");
    div.innerHTML = "";
    for(var i = 0; i < data.length; i++)
    {
        if(data[i].from_ != undefined)
        {
            var template = `<div class="card mb-3" style="max-width: 540px;">
            <div class="row no-gutters">
              <div class="col-md-4">
                <img src="static/img/1917.jpg" class="card-img" alt="...">
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">${data[i].theatre_name}</h5>
                  <p class="card-text">
                  <strong>Date:</strong> ${data[i].date_}   
                  <strong>Time:</strong> ${data[i].time}<br>
                  <strong>Movie Name: </strong>${data[i].movie_name}<br>
                  <strong>Tickets: </strong>${data[i].tickets} <br>
                  <strong>Price: </strong>Rs.${data[i].price} <br>
                  </p>
                </div>
              </div>
            </div>
          </div>`
        }
        else
        {
            var template = `<div class="card mb-3" style="max-width: 540px;">
            <div class="row no-gutters">
              <div class="col-md-4">
                <img src="static/img/cancelled.png" class="card-img" alt="...">
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">Cancelled</h5>
                  <p class="card-text">
                  <strong>Tickets: </strong>${data[i].tickets} <br>
                  <strong>Price: </strong>Rs.${data[i].price} <br>
                  <strong>Refund Initiated</strong> <br>
                  </p>
                </div>
              </div>
            </div>
          </div>`
        }
        div.innerHTML += template;
    }

}

async function my_account()
{
    var url = `http://192.168.1.8:5000/book`;

    try{
        var response = await fetch(url);
        var data = await response.json();
        console.log(data);
        if(data)
        {
            create_my_account_divs(data);
        }
        
    }
    catch(error) {
        console.log(error);
    }
}

async function book_tickets(id, price, tickets)
{
    console.log('here');
    var modal = document.getElementById('myModal');
    modal.style.display = "block";

    var span = document.getElementsByClassName("close")[0];
    span.onclick = function() {
        modal.style.display = "none";
    }

    var price_span = document.getElementById("price");
    var ticket_input = document.getElementById("number");

    var book_button = document.getElementById("confirm");

    book_button.onclick = async function() {
        var ticket = parseInt(ticket_input.value);
        if(ticket > tickets)
        {
            alert("Not enough tickets");
        }
        else
        {
            var url = `http://192.168.1.8:5000/book?id=${id}&ticket=${ticket}`;
            try
            {
                var response = await fetch(url, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({id: id, ticket: ticket, price: price * ticket})
                });

                if (response) {
                    var data = await response.json();
                    console.log(data);
                    alert("Ticket booked successfully");
                    modal.style.display = "none";
                }
                else {
                    alert("Error booking Ticket");
                    modal.style.display = "none";
                }
                location.reload();
            }
            catch(error)
            {
                console.log(error);
                modal.style.display = "none";
            }
        }
    }

    // ticket_input.onchange = function()
    // {
    //     console.log(ticket_input.value, price);
    //     var cost = parseInt(price) * parseInt(ticket_input.value);
    //     price_span.innerHTML = "Price : Rs. " + cost;
    // }

    ticket_input.addEventListener('input', function() {
        console.log(ticket_input.value, price);
        var cost = parseInt(price) * (parseInt(ticket_input.value) || 0);
        price_span.innerHTML = "Price : Rs. " + cost;
    });

}

async function add_movie()

{
     theatre_name = document.getElementById('theatre_name').value;
     movie_name = document.getElementById('movie_name').value;
     date = document.getElementById('date').value;
     theatre_time = document.getElementById('theatre_time').value;
     price = document.getElementById('price').value;

    var url = `http://192.168.1.8:5000/add_movie?theatre_name=${theatre_name}&movie_name=${movie_name}&date=${date}&time=${theatre_time}&price=${price}`
    var movie = {
        theatre_name: theatre_name,
        movie_name:movie_name,
        date:date,
        time:theatre_time,
        price:price
    }

    try{
        var response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(movie)
        });

        if (response) {
            var data = await response.json();
            // console.log(data);
            alert("Movie added successfully");
        }
        else {
            alert("Error adding Movie");
        }
    }
    catch(error) {
        console.log(error);
    }

    

}
    

function create_divs(data, op)
{
    var div = document.getElementById("results");
    div.innerHTML = "";
    for(var i = 0; i < data.length; i++)
    {
        if(op == "search")
        {
            const date = data[i]['date'].split(/(\s+)/);
            var template = `<div class="card" style="width: 18rem;">
            <img class="card-img-top" src="static/img/1917.jpg" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">${data[i]['movie_name']}</h5>
              <p class="card-text">Movie Name : ${data[i]['name']}</p>
              <h6 class="card-subtitle mb-2 text-muted">Rs.${data[i].price}</h6>
              
            </div>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">Theatre : ${date[i]['theatre_name']}</li>
              <li class="list-group-item">Date : ${date[0]}</li>
              <li class="list-group-item">Time : ${data[i]['time']}</li>
              <li class="list-group-item">Tickets : ${data[i]['tickets']}</li>
            </ul>
            
            <div class="card-body">
                <button class="btn btn-dark" onclick="book_tickets(${data[i].id},${data[i].price}, ${data[i].tickets})">Book</button>
            </div>
          </div>`
        }
        else if(op == "view")
        {
            headDIV = document.getElementById("detailheader");
            headDIV.style.display = "none";
            const date = data[i]['date'].split(/(\s+)/);
            var template = `<div class="card" style="width: 18rem;">
            <img class="card-img-top" src="static/img/jonny_english.jpg" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">${data[i]['movie_name']}</h5>
              <h6 class="card-subtitle mb-2 text-muted">Rs.${data[i].price}</h6>
              <p class="card-text">Movie Name : ${data[i]['movie_name']}</p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">Date : ${date[0]}</li>
              <li class="list-group-item">Time : ${data[i]['time']}</li>
              <li class="list-group-item">Tickets : ${data[i]['tickets']}</li>
            </ul>
            
            <div class="card-body">
                <button class="btn btn-dark" onclick="view(${data[i]['id']})">View</button>
            </div>
          </div>`
        }

      div.innerHTML += template;
    }
}

async function search(op)
{
    var theatre_name = document.getElementById("theatre").value
    var movie_name  = document.getElementById("movie_name").value
    var date = document.getElementById("date").value

    

    var url = `http://192.168.1.8:5000/search?theatre_name=${theatre_name || " "}&movie_name=${movie_name || " "}&date=${date || " "}`;
    
    var body = 
    {
        theatre_name: theatre_name || " ",
        movie_name: movie_name || " ",
        date: date || " "
    }
    console.log(body);
    try{
        var response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response) {
            var data = await response.json();
            console.log(data);
            if(data)
            {
                create_divs(data, op);
            }

            
        }
    
    }
    catch(error) {
        console.log(error);
    }
}


async function add_theatre()
{
    theatre_name        = document.getElementById("theatre_name").value 
    theatre_district    = document.getElementById("theatre_district").value
    theatre_state       = document.getElementById("theatre_state").value

    var url = `http://192.168.1.8:5000/add_theatre?theatre_name=${theatre_name}&theatre_district=${theatre_district}&thretre_state=${theatre_state}`;
    var theatre = {
        theatre_name: theatre_name,
        theatre_district:theatre_district,
        theatre_state:theatre_state
    };

    try{
        var response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(theatre)
        });

        if (response) {
            var data = await response.json();
            console.log(data);
            alert("Theatre added successfully");
        }
        else {
            alert("Error adding theatre");
        }
    }
    catch(error) {
        console.log(error);
    }

    // create api call
    
}

