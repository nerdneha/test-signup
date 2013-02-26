<p> Please sign in below! </p>
%#endif
<form action="/signup" method="POST">
  <table>
    <tr>
      <td>Username: </td>
      <td> <input type="text" size="50" maxlength="50" name="username"> </td>
      <td>{{user_error}}
    </tr>
    <tr>
      <td>Password: </td>
      <td> <input type="password" size="50" maxlength="50" name="password">
      </td>
    </tr>
    <tr>
      <td>Confirm Password: </td>
      <td> <input type="password" size="50" maxlength="50" name="passwordconf">
      </td>
      <td> {{pw_error}} </td>
    </tr>
    <tr>
      <td>What food do you like?: </td>
      <td><input type="text" size="50" maxlength="50" name="food"> </td>
    </tr>
  </table>
  <input type="submit" name="submit" value="save">
</form>
