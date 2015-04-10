// Generated by CoffeeScript 1.9.1
(function() {
  "use strict";

  /*
    Handle the Login using Username and ApiKey
   */
  (function($) {
    var $loginModalButton, $userLoginButton, currentUser, getUserInfo, handleLogout, setLogout;
    currentUser = User.getCurrentUser();
    $loginModalButton = $("#loginButton");
    $userLoginButton = $('#userLoginButton');

    /*
      Activate tooltips on links
     */
    $("a[data-toggle='tooltip']").tooltip();

    /*
      FUNCTION BLOCK
     */
    setLogout = function() {
      return $('#userLoginButton').html("Logout").attr('data-logout', true);
    };

    /*
      Retrieve the user info
     */
    getUserInfo = function() {
      var admin, apikey, username;
      username = $("#username").val();
      apikey = $("#apikey").val();
      admin = $("#adminCheck").is(":checked");
      if (!username || !apikey) {
        $("#emptyAlert").fadeIn();
        return false;
      } else {
        $("#emptyAlert").fadeOut();
      }
      currentUser.setInfo(username, apikey, admin);
      return true;
    };

    /*
      Remove data from the localstorage and logout the user
     */
    handleLogout = function() {
      return currentUser.clearInfo();
    };

    /*
      check if already logged in with LocalStorage
     */
    if (currentUser.isValid()) {
      $("#username").val(currentUser.name);
      $("#apikey").val(currentUser.apikey);
      if (currentUser.admin) {
        $("#adminCheck").prop('checked', true);
      }
      setLogout();
    }

    /*
      BUTTON MANAGEMENT
     */
    $loginModalButton.click(function(e) {
      e.preventDefault();
      if (getUserInfo()) {
        $("#loginModal").modal("hide");
        return setLogout();
      }
    });
    $userLoginButton.click(function(e) {
      e.preventDefault();
      if ($(this).attr("data-logout")) {
        return handleLogout();
      } else {
        return $("#loginModal").modal("show");
      }
    });
    return $(currentUser).on('user.logout', function() {
      return $userLoginButton.html("Login").removeAttr('data-logout');
    });
  })(jQuery);

}).call(this);

//# sourceMappingURL=loginLogout.js.map
