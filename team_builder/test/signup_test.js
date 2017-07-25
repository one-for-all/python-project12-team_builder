describe('signup', function() {
  let server;
  let data;
  before(function () {
    server = sinon.fakeServer.create();
    data = {
      'username': 'test',
      'email': 'test@example.com',
      'password': 'password',
      'confirm': 'password'
    };
  });
  after(function () { server.restore();});
  it('should send data to signup api URL', function() {
    server.respondWith('POST', '/accounts/api/v1/signup/', [200, {
      "Content-Type": "application/json"},
      `{
        "account": {
          "username": "test",
          "email": "test@example.com"
        }
      }`
    ]);
    signup(data);
    server.respond();
    expect(JSON.parse(server.requests[0].requestBody)).to.eql(data);
  });
});
