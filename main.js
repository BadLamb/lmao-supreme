const base_url = "http://supremenewyork.com"

const options = {
    name: "Luca Todesco",
    email: "supreme@cocaine.ninja",
    tel: "+39 123456789",
    city: "Venice",
    zip: "123456",
    country: "ITALY",
    address: "idk lol 69",
    type: "visa",
    cc: "1234567891234567",
    cvv: "892",
    expm: "07",
    expy: "2019",
}

let Nightmare = require('nightmare');
let nightmare = Nightmare({
    show: true,
    typeInterval: 1,
});

let exec = require('child_process').exec;

let available = []

exec("python available.py", (error, stdout, stderr) => {
    available = stdout.split('\n')
    nightmare
        .goto(base_url + available[2])
        .click("#add-remove-buttons > input")
        .wait(100)
        .click("#cart > a.button.checkout")

    buy_product()
})

let buy_product = () => {
    nightmare
        .wait("#order_billing_name")
        .type("#order_billing_name", options.name)
        .type("#order_email", options.email)
        .type("#order_tel", options.tel)
        .type("#order_billing_city", options.city)
        .type("#bo", options.address)
        .type("#order_billing_zip", options.zip)
        .type("#order_billing_country", options.country)
        .type("#credit_card_month", options.expm)
        .type("#credit_card_year", options.expy)
        .type("#vval", options.cvv)
        .type("#credit_card_type", options.type[0])
        .click("#cart-cc > fieldset > p > label > div > ins")
        .inject('js', 'captcha_bypass.js')
        .wait("#confirmation")
        .catch(e => {
            console.log(e)
          })
        }
