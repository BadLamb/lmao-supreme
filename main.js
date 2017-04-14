const base_url = "http://supremenewyork.com"
const bot_token = ""

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

const Nightmare = require('nightmare');
const nightmare = Nightmare({
    show: true,
    typeInterval: 1,
    webPreferences: {
        images: false,
    }
});

let id = 0;
const exec = require('child_process').exec;

const TelegramBot = require('node-telegram-bot-api');
const bot = new TelegramBot(bot_token, {polling: true});

bot.on('message', (msg) => {
    id = msg.chat.id
    console.log("done")
})

let available = []
let start = 0
exec("python available.py", (error, stdout, stderr) => {
    available = stdout.split('\n')
    start = +new Date();
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
        .screenshot("done.png")
        .then(() => {
            let end = +new Date();
            let t = (end-start)/1000
            bot.sendMessage(id, "Fucking done it bro, took " + t.toString() + "s")
            bot.sendDocument(id, "done.png")
            setTimeout(() => {
                process.exit()
            }, 1000)
        })
        .catch(e => {
            console.log(e)
          })
        }
