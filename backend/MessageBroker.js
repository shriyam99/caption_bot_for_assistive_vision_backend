var amqp = require('amqplib')

let instance;

class MessageBroker{

    async init(){
      this.connection = await amqp.connect('amqp://localhost');
      this.channel = await this.connection.createChannel();
       return this
    }


    async send(queue, msg) {
      if (!this.connection) {
        await this.init();
      }
      await this.channel.assertQueue(queue, {durable: true});
      this.channel.sendToQueue(queue, msg)
  }

}




MessageBroker.getInstance = async function() {
    if (!instance) {
      const broker = new MessageBroker();
      instance = broker.init()
    }
    return instance;
  };

  module.exports = MessageBroker;