"use strict"
###
  Represent the User in the application
###
(($) ->
  class User
    constructor: (@name, @apikey, @admin) ->
    saveLocalStorage: () ->
      localStorage.setItem('User', JSON.stringify(this))
    setInfo: (@name, @apikey, @admin) ->
      this.saveLocalStorage()
      $(this).trigger('user.login');
    isValid: () ->
      return this.name && this.apikey && this.admin
    clearInfo: () ->
      delete this.apikey
      delete this.name
      delete this.admin
      localStorage.removeItem('User')
      $(this).trigger('user.logout');
    @fromLocalStorage: () ->
      localUser = localStorage.getItem('User')
      if localUser
        localObject = new User()
        $.extend(localObject, JSON.parse(localUser))
        return localObject
      return new User()
    @currentUser : null
    @getCurrentUser: () ->
      return this.currentUser ? this.currentUser = User.fromLocalStorage()

  root = window ? this
  root.User = User
) jQuery