end_point_url = "http://127.0.0.1:5000"

class User {
    // User_id & Access_token are preset within cookies
    constructor(event = false) {
        if(event){
            event.preventDefault()
        }
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
                location.href = "home.html"
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
        var data = {
            "company_name": form["company_name"].value,
            "phone": form["phone"].value,
            "email": form["email"].value,
            "till_number": form["till"].value,
            "bank_account": form["bank"].value,
            "crypto": form["crypto"].value,
        }
        console.log(data)
        fetch(`${this.url}/account_update`, this.PrepFetch(data))
        .then(x => x.json())
        .then(y => {
            if (!y["state"]) {
                console.log(y["message"])
                if (y["message"] === "AuthToken Error") {
                    location.href = "signin.html"
                }
                // Alert user using the message key to know why signin failed
            }
            console.log(y)
            this.StoreJSONData(y["data"])
            setTimeout(()=>{
                location.href = "profile.html"
            })
        })
    }

    RenderJOSNtoDom(parent_element, parent_element_payment) {
        var account = this.FetchAccountUserData()
        console.log(account.company_name)
        if(account.company_name == "Invalid") {
            location.href = "signin.html"
        }
        var textContext =
            `<div class="row mx-0 mb-3">
        <div class="col-6 p-0">
            <small class="text-muted mb-1 f-10 pr-1">Phone</small>
            <p class="small mb-0 l-hght-14">${account["phone"]}</p>
        </div>
        <div class="col-6 p-0">
            <small class="text-muted mb-1 f-10 pr-1">Email</small>
            <p class="small mb-0 l-hght-14">${account["email"].substring(0,10)}*****</p>
        </div>
    </div>
    <div class="row mx-0 mb-3">
        <div class="col-6 p-0">
            <small class="text-muted mb-1 f-10 pr-1">Means Type</small>
            <p class="small mb-0 l-hght-14">${account["means_type"]}</p>
        </div>
        <div class="col-6 p-0">
            <small class="text-muted mb-1 f-10 pr-1">Log In Accounts</small>
            <p class="small mb-0 l-hght-14">${account["log_acc"]}</p>
        </div>
    </div>
    <div class="row mx-0">
        <div class="col-6 p-0">
            <small class="text-muted mb-1 f-10 pr-1">Verification</small>
            <p class="small mb-0 l-hght-14">${account["verification"]}</p>
        </div>
        <div class="col-6 p-0">
            <small class="text-muted mb-1 f-10 pr-1">Status</small>
            <p class="small mb-0 l-hght-14">${account["status"]}</p>
        </div>
    </div>`
        parent_element.innerHTML = textContext
        document.getElementById('company_name').innerHTML = account["company_name"]

        console.log("siniwqxoiq")


        parent_element_payment.innerHTML = ""
        var payment_context = ""
        // mpesa
        if(account["payment"][0]){
            payment_context += `
            <div class="border-bottom p-3">
                    <div class="w-100 mastercard custom-control custom-radio custom-control-inline mr-0">
                            <a href="payment-card.html" class="d-flex align-items-start">
                                <div class>
                                    <p class="mb-0 text-dark">M-Pesa</p>
                                    <small class="text-muted">Till Number: ${account["payment"][0]}</small><br>
                                    <small class="text-muted">Get payment from Global M-Pesa Clients directly to your till number</small>
                                </div>
                                <img style="width: 15%" src="data:image/png;base64,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" class="img-fluid rounded ml-auto">
                            </a>
                        </label>
                    </div>
            </div> `
        }

        // bank
        if(account["payment"][1]){
            payment_context += `
            <div class="border-bottom p-3">
                    <div class="w-100 mastercard custom-control custom-radio custom-control-inline mr-0">
                            <a href="payment-card.html" class="d-flex align-items-start">
                                <div class>
                                    <p class="mb-0 text-dark">Bank Account</p>
                                    <small class="text-muted">Account No.: ${account["payment"][1]}</small><br>
                                    <small class="text-muted">Pay from mastercard account using mastercard payment gateway</small>
                                </div>
                                <img src="img/master.png" class="img-fluid rounded ml-auto">
                            </a>
                        </label>
                    </div>
            </div> `
        }

        // crypto
        if(account["payment"][2]){
            payment_context += `
            <div class="border-bottom p-3">
                    <div class="w-100 mastercard custom-control custom-radio custom-control-inline mr-0">
                            <a href="payment-card.html" class="d-flex align-items-start">
                                <div class>
                                    <p class="mb-0 text-dark">Crypto Address</p>
                                    <small class="text-muted">Crypto: ${account["payment"][2]}</small><br>
                                    <small class="text-muted">Pay from mastercard account using mastercard payment gateway</small>
                                </div>
                                <img src="img/master.png" class="img-fluid rounded ml-auto">
                            </a>
                        </label>
                    </div>
            </div> `
        }

        parent_element_payment.innerHTML = payment_context

    }

    StoreJSONData(json_data) {
        localStorage.setItem("db_data", JSON.stringify(json_data))
    }

    FetchAccountUserData() {
        var response = {
            "company_name": "Invalid",
            "phone": "Invalid",
            "email": "Invalid",
            "means_type": "Invalid",
            "log_acc": "Invalid",
            "verification": "Invalid",
            "status": "Invalid",
            "payment": []
        }
        var db_data = localStorage.getItem("db_data")
        db_data = JSON.parse(db_data)
        console.log(db_data)
        if(!db_data){return response}

        response.company_name = db_data["account_profile"]["company_name"]
        response.phone = db_data["account_profile"]["phone"]
        response.email = db_data["account_profile"]["email"]
        response.means_type = db_data["account_profile"]["means_type"]
        response.log_acc = 1
        response.verification = db_data["account_profile"]["verification"]
        response.status = db_data["account_profile"]["verification"]
        response.payment = [
            db_data["account_profile"]["payment_methods"]["Mpesa"],
            db_data["account_profile"]["payment_methods"]["BankAccount"],
            db_data["account_profile"]["payment_methods"]["CryptoAddress"],
        ]
        return response
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

    CreateDBStructure() {
        var structure = {
            "account_profile": "",
            "buses": null,
            "drivers": null
        }
        localStorage.setItem("db_data", JSON.stringify(structure))
    }

    EditUserProfile(form){
        var account_details = this.FetchAccountUserData()
        console.log(account_details)
        form["company_name"].value = account_details["company_name"]
        form["phone"].value = account_details["phone"]
        form["email"].value = account_details["email"]
        form["till"].value = account_details["payment"][0]
        form["bank"].value = account_details["payment"][1]
        form["crypto"].value = account_details["payment"][2]
    }
}

bus_url = "add"
current_bus_id = ""

class Buses {
    constructor(event = false) {
        if (event) {
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

        if (bus_url === "update") {
            this.UpdateBus()
            return
        }
        fetch(`${this.url}/bus/add`, this.PrepFetch(data))
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

    DeleteBus(bus_id) {
        var data = {
            "bus_id": bus_id
        }
        if (!confirm("Are you sure to delete vehicle ?")) { return }
        fetch(`${this.url}/bus/delete`, this.PrepFetch(data))
        .then(x => x.json())
        .then(y => {
            console.log(y)
            if (!y["state"]) {
                if (y["message"] === "AuthToken Error") {
                    location.href = "signin.html"
                }
            }
            alert("Vehicle Deleted Successfully")
            this.StoreJSONBusData(y["data"])
        })
    }

    UpdateBus() {
        var form = document.forms["bus_form"]
        var bus_id = current_bus_id
        var licesnse_plate = form["licesnse_plate"].value
        var no_seats = form["no_seats"].value
        var model = form["model"].value
        var colour = form["colour"].value
        var seat_config = form["seat_config"].value
        var data = {
            "bus_id": bus_id,
            "licesnse_plate": licesnse_plate,
            "no_seats": no_seats,
            "model": model,
            "colour": colour,
            "seat_config": seat_config
        }
        fetch(`${this.url}/bus/update`, this.PrepFetch(data))
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

    EditBusdetails(bus_id) {
        var db_data = localStorage.getItem("db_data")
        db_data = JSON.parse(db_data)
        var all_buses = db_data["buses"]
        for (var x in all_buses) {
            if (all_buses[x][0] === bus_id) {
                current_bus_id = bus_id
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
                                <p class="small mb-1">${all_buses[bus][8] === 1 ? "BOOKED" : "UNBOOKED"}</p>
                            </div>
                        </div>
                        <button class="col-5 p-2 rounded-2 bg-danger text-white ring-0 mt-2" onclick="new Buses().EditBusdetails('${all_buses[bus][0]}')">Edit</button>
                        <button class="col-5 p-2 rounded-2 bg-tomato text-white ring-0 mt-2" onclick="new Buses().DeleteBus('${all_buses[bus][0]}')">Delete</button>
                    </div>
                </div>
            </div>
                </div>`
            rendered_buses += unit_bus
        }

        parent_element.innerHTML = ""
        parent_element.innerHTML = rendered_buses
    }

    StoreJSONBusData(bus_data) {
        var db_data = localStorage.getItem('db_data')
        db_data = JSON.parse(db_data)
        db_data["buses"] = bus_data
        localStorage.setItem('db_data', JSON.stringify(db_data))
        new Buses().RenderJSONtoDOM(document.getElementById('all_buses_display'))
    }

    CloseAddBusForm() {
        document.getElementById('new-bus-form').style.display = 'none'
    }

    OpenAddBusForm(bus_data) {
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

