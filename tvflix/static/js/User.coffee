"use strict"
###
  Represent the User in the application
###
(($) ->
  class User
    constructor: (@name, @apikey) ->
    saveLocalStorage: () ->
      localStorage.setItem('User', JSON.stringify(this))
    setInfo: (@name, @apikey) ->
      this.saveLocalStorage()
      $(this).trigger('user.login');
    isValid: () ->
      return this.name != null && this.apikey != null
    clearInfo: () ->
      delete this.apikey
      delete this.name
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