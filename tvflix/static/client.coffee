username = localStorage.getItem("username")
apikey = localStorage.getItem ("apikey")
(($) ->
  ###
    FUNCTION BLOCK
  ###
  setLogout = ->
    $('#userLoginButton').html("Logout").attr('data-logout', true)
  ###
    Retrieve the user info
  ###
  getUserInfo = ->
    username = $("#username").val()
    apikey = $("#apikey").val()

    if !username || !apikey
      $("#emptyAlert").fadeIn()
      return false
    else
      $("#emptyAlert").fadeOut();

    #Save in local storage
    localStorage.setItem("username", username)
    localStorage.setItem('apikey', apikey)
    return true
  ###
    Remove data from the localstorage and logout the user
  ###
  handleLogout = ->
    username = null
    apikey = null
    localStorage.removeItem("username")
    localStorage.removeItem("apikey")
    $(this).html("Login").removeAttr('data-logout')
  ###
    check if already logged in with LocalStorage
  ###
  if username && apikey
    setLogout()

  ###
    BUTTON MANAGEMENT
  ###

  $("#loginButton").click (e) ->
    e.preventDefault()
    if getUserInfo()
      $("#loginModal").modal("hide")
      setLogout()

  $('#userLoginButton').click (e) ->
    e.preventDefault()
    if $(this).attr("data-logout")
      handleLogout.call(this)
    else
      $("#loginModal").modal("show")) jQuery