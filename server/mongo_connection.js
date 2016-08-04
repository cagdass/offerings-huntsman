var mongo = require('mongodb').MongoClient
var default_url = 'mongodb://127.0.0.1:27017/users'

var mongoPromise = mongo.connect(default_url)
  .catch(function(error){
    console.error(error);
    throw error
  })

var mongo_service = {
  connect: function(url){
    url = url || default_url;
    return mongo.connect(url)
    .catch(function(error){
      console.error(error);
      throw error
    })
  }, getUserCollection: function(){
    return mongoPromise
    .then(function(db){
      var user_collection = db.collection("users");
      return user_collection;
    });
  }
}

module.exports = mongo_service

