var mongo_service = require('./mongo_connection')
var Promise = require("bluebird");

function schedule_service(db){
  var service = this;
  // var mongo = require('mongodb')
  var validate = require('validate.js')
  // var constraints = require('./user_constraints');

  // Find all classes from a professor.
  service.find_classes_from_instructor = function(professor){
    var name = professor.instructor.replace("%20", " ");
    console.log("Finding classes of " + name);
    return Promise.try(function(){
      return mongo_service.getCollection()
      .then(function(collection){
        // return collection.find({"instructor": {"$regex": "Davenport"}}).toArray();
        return collection.find({"instructor": {"$regex": name}}).toArray();
      })
    })
  };

  // Find all classes of a department.
  service.find_classes_from_department = function(departmentCode){
    console.log("Finding classes from department " + departmentCode.departmentCode);
    return Promise.try(function(){
      return mongo_service.getCollection()
      .then(function(collection){
        return collection.find(departmentCode).toArray()
      })
    })
  };

  // Find distinct departments
  service.find_distinct_departments = function(){
    console.log("Retrieving distinct departments.");
    return Promise.try(function(){
      return mongo_service.getCollection()
      .then(function(collection){
        return collection.distinct("departmentCode")
      })
    })
  };

  // Find classes that are in this classroom.
  service.find_classroom = function(classroom){
    console.log("Finding classroom " + JSON.stringify(classroom));
    return Promise.try(function(){
      // var not_validated = validate(user, constraints.constraints)
      return mongo_service.getCollection()
      .then(function(collection){
        return collection.find(classroom).toArray()
      })
    })
  };
}

module.exports = schedule_service
