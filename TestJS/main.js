end_point_url = "http://127.0.0.1:5000"

class User{
    // User_id & Access_token are preset within cookies
    constructor(event) {
        event.preventDefault()
        this.url = `${end_point_url}`
    }

    SignUp(form){
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

        if(password_1 != password_2){
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
        .then(x=>x.json())
        .then(y=>{
            if(!y["state"]){
                console.log(y["message"])
                // Alert user using the message key to know why signup failed
            }
            console.log(y)
            this.RenderJSONData(y["data"])
        })

    }

    SignIn(form){
        var email = form["email"].value
        var password = form["password"].value
        if(email.length === 0 && password.length === 0){
            alert("missing data")
            return
        }

        var data = {
            "email": email,
            "password": password
        }

        fetch(`${this.url}/signin`, this.PrepFetch(data))
        .then(x=>x.json())
        .then(y=>{
            if(!y["state"]){
                console.log(y["message"])
                if(y["message"] === "Authentication Failed"){
                    var original_color = form["password"].style.borderColor
                    form["password"].style.borderColor = "red"
                    setTimeout(()=>{
                        form["password"].style.borderColor = original_color
                    }, 1500)
                }else{
                    alert(y["message"])
                }
                return
                // Alert user using the message key to know why signin failed
            }

            console.log(y)
            this.RenderJSONData(y["data"])
            location.href = "home.html"
        })


    }

    UpdateProfile(form){
        console.log("testing function")
    }

    RenderJSONData(json_data){
        this.PrepFetch()
    }

    PrepFetch(data){
        var options = {
            method: 'POST',
            credentials: 'include',
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        return options
    }
}


class Buses{
    constructor(event) {
        event.preventDefault()
        this.url = `${end_point_url}`
    }

    AddBus(form){
        var licesnse_plate = form[""]
        var no_seats = ""
        var model = ""
        var colour = ""
        var seat_config = ""
    }
}
