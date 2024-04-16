end_point_url = "http://127.0.0.1:5000"

class User {
    // User_id & Access_token are preset within cookies
    constructor(event) {
        event.preventDefault()
        this.url = `${end_point_url}`
    }

    SignUp(form) {
        var logo = form["logo"]
        var name = form["name"].value
        var phone = form["phone"].value
        var email = form["email"].value
        var means_type = form["means_type"].value
        var till_number = form["till_number"].value
        var bank_account = form["bank_account"].value
        var crypto_wallet = form["crypto_wallet"].value
        var password_1 = form["password_1"].value
        var password_2 = form["password_2"].value

        if (password_1 != password_2) {
            console.log("Miss Match")
            form["password_1"].style.borderColor = "red"
            form["password_2"].style.borderColor = "red"
            return
        }

        var data = {
            "logo": logo.files[0],
            "company_name": name,
            "phone": phone,
            "email": email,
            "means_type": means_type,
            "till_number": till_number,
            "bank_account": bank_account,
            "crypto_wallet": crypto_wallet,
            "password": password_1
        }

        console.log(this.PrepFetch(data))
        fetch(`${this.url}/signup`, this.PrepFetch(data))
            .then(x => x.json())
            .then(y => {
                if (!y["state"]) {
                    console.log(y["message"])
                    // Alert user using the message key to know why signup failed
                }
                console.log(y)
                this.CreateDBStructure()
            })
    }

    SignIn(form) {
        var email = form["email"].value
        var password = form["password"].value
        if (email.length === 0 && password.length === 0) {
            alert("missing data")
            return
        }

        var data = {
            "email": email,
            "password": password
        }

        fetch(`${this.url}/signin`, this.PrepFetch(data))
            .then(x => x.json())
            .then(y => {
                if (!y["state"]) {
                    console.log(y["message"])
                    if (y["message"] === "Authentication Failed") {
                        var original_color = form["password"].style.borderColor
                        form["password"].style.borderColor = "red"
                        setTimeout(() => {
                            form["password"].style.borderColor = original_color
                        }, 1500)
                    } else {
                        alert(y["message"])
                    }
                    return
                    // Alert user using the message key to know why signin failed
                }

                console.log(y)
                this.StoreJSONData(y["data"])
                location.href = "home.html"
            })


    }

    UpdateProfile(form) {
        console.log("testing function")
    }

    StoreJSONData(json_data) {
        localStorage.setItem("db_data", JSON.stringify(json_data))
    }

    PrepFetch(data) {
        var options = {
            method: 'POST',
            credentials: 'include',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        return options
    }

    CreateDBStructure(){
        var structure = {
            "account_profile": "",
            "buses": null,
            "drivers": null
        }
        localStorage.setItem("db_data", JSON.stringify(structure))
    }
}

bus_url = "add"
class Buses {
    constructor(event=false) {
        if(event){
            event.preventDefault()
        }
        this.url = `${end_point_url}`
        this.bus_id = ""
    }

    AddBus(form) {
        var licesnse_plate = form["licesnse_plate"].value
        var no_seats = form["no_seats"].value
        var model = form["model"].value
        var colour = form["colour"].value
        var seat_config = form["seat_config"].value
        var data = {
            "licesnse_plate": licesnse_plate,
            "no_seats": no_seats,
            "model": model,
            "colour": colour,
            "seat_config": seat_config
        }

        alert(bus_url)
        fetch(`${this.url}/bus/${this.bus_url}`, this.PrepFetch(data))
        .then(x => x.json())
        .then(y => {
            console.log(y)
            if (!y["state"]) {
                if (y["message"] === "AuthToken Error") {
                    location.href = "signin.html"
                }
            }
            this.StoreJSONBusData(y["data"])
            this.CloseAddBusForm()
        })
    }

    DeleteBus(bus_id){
        var data = {
            "bus_id": bus_id
        }

        fetch(`${this.url}/bus/delete`, this.PrepFetch(data))
        .then(x=>x.json())
        .then(y=>{
            console.log(y)
            if (!y["state"]) {
                if (y["message"] === "AuthToken Error") {
                    location.href = "signin.html"
                }
            }
            this.StoreJSONBusData(y["data"])
        })
    }

    UpdateBus(){
        var licesnse_plate = form["licesnse_plate"].value
        var no_seats = form["no_seats"].value
        var model = form["model"].value
        var colour = form["colour"].value
        var seat_config = form["seat_config"].value
        var data = {
            "licesnse_plate": licesnse_plate,
            "no_seats": no_seats,
            "model": model,
            "colour": colour,
            "seat_config": seat_config
        }
        fetch(`${this.url}/bus/${bus_url}`, this.PrepFetch(data))
        .then(x=>x.json())
        .then(y=>{
            console.log(y)
            if (!y["state"]) {
                if (y["message"] === "AuthToken Error") {
                    location.href = "signin.html"
                }
            }
            this.StoreJSONBusData(y["data"])
        })
    }

    EditBusdetails(bus_id){
        var db_data = localStorage.getItem("db_data")
        db_data = JSON.parse(db_data)
        var all_buses = db_data["buses"]
        for(var x in all_buses){
            if(all_buses[x][0] === bus_id){
                this.OpenAddBusForm(all_buses[x])
            }
        }
    }

    PrepFetch(data) {
        var options = {
            method: 'POST',
            credentials: 'include',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        return options
    }

    RenderJSONtoDOM(parent_element) {
        // JSON.parse(localStorage.getItem("db_data"))
        var db_data = localStorage.getItem("db_data")
        if (!db_data) { return }
        db_data = JSON.parse(db_data)

        var all_buses = db_data["buses"]
        var rendered_buses = `
        <div class="p-2 border-bottom w-100">
                <div class="bg-white border border-warning rounded-1 shadow-sm p-2">
                    <div class="row mx-0 px-1">
                        <div class="col-6 p-0">
                            <small class="text-muted mb-1 f-10 pr-1">BOOKED</small>
                            <p class="small mb-0">${all_buses.length} Buses</p>
                        </div>
                        <div class="col-6 p-0">
                            <small class="text-muted mb-1 f-10 pr-1">UNOCCUPIED</small>
                            <p class="small mb-0">${all_buses.length} Buses</p>
                        </div>
                    </div>
                </div>
            </div>`
        console.log(db_data)

        for (var bus in all_buses) {
            var unit_bus = `<div class="text-dark col-11 px-0 mt-2">
            <div class="list_item_gird m-0 bg-white shadow-sm listing-item border-bottom border-right">
                <div class="px-3 pt-3 tic-div">
                    <div class="list-item-img">
                        <img src="img/listing/item1.png" class="img-fluid">
                    </div>
                    <p class="mb-0 l-hght-10">${all_buses[bus][4]}</p>
                    <span class="text-danger small">${all_buses[bus][2]}</span>
                </div>
                <div class="p-3 d-flex justify-content-center">
                    <div class="bus_details w-100 row justify-content-around">
                        <div class="d-flex col-12">
                            <p><i class="icofont-chair mr-2 text-danger"></i><span class="small">${all_buses[bus][3]} Seats</span></p>
                            <p class="small ml-auto"><i class="icofont-color-bucket mr-2 text-danger"></i>${all_buses[bus][5]}</p>
                        </div>
                        <div class="d-flex l-hght-10 col-12">
                            <span class="icofont-bus-alt-1 small mr-2 text-danger"></span>
                            <div>
                                <small class="text-muted mb-2 d-block">No. of Trips</small>
                                <p class="small">${all_buses[bus][7]}</p>
                            </div>
                            
                        </div>
                        <div class="d-flex l-hght-10 col-12">
                            <span class="icofont-google-map small mr-2 text-danger"></span>
                            <div>
                                <small class="text-muted mb-2 d-block">Status</small>
                                <p class="small mb-1">${all_buses[bus][8] === 1 ? "BOOKED": "UNBOOKED"}</p>
                            </div>
                        </div>
                        <button class="col-5 p-2 rounded-2 bg-danger text-white ring-0 mt-2" onclick="new Buses().EditBusdetails('${all_buses[bus][0]}')">Edit</button>
                        <button class="col-5 p-2 rounded-2 bg-tomato text-white ring-0 mt-2" onclick="new Buses().DeleteBus('${all_buses[bus][0]}')">Delete</button>
                    </div>
                </div>
            </div>
                </div>`
            rendered_buses +=unit_bus
        }
        
        parent_element.innerHTML = ""
        parent_element.innerHTML = rendered_buses
    }

    StoreJSONBusData(bus_data){
        var db_data = localStorage.getItem('db_data')
        db_data = JSON.parse(db_data)
        db_data["buses"] = bus_data
        localStorage.setItem('db_data', JSON.stringify(db_data))
        console.log(db_data)
        new Buses().RenderJSONtoDOM(document.getElementById('all_buses_display'))
    }

    CloseAddBusForm(){
        document.getElementById('new-bus-form').style.display = 'none'
    }

    OpenAddBusForm(bus_data){
        this.bus_id = bus_data[0]
        var bus_form = document.forms["bus_form"]
        console.log(bus_form)
        bus_url = "update"
        bus_form["licesnse_plate"].value = bus_data[2]
        bus_form["no_seats"].value = bus_data[3]
        bus_form["model"].value = bus_data[4]
        bus_form["colour"].value = bus_data[5]
        bus_form["seat_config"].value = bus_data[6]
        document.getElementById('new-bus-form').style.display = 'block'
    }
}
