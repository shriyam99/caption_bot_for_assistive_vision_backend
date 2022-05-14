const rabbit = require('./MessageBroker.js')

const send = async (ctx) => {
  const broker = await rabbit.getInstance()
  console.log("Sended")
  await broker.send('test', Buffer.from(ctx))
}

exports.send = send