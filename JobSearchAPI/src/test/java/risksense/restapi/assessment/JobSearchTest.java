package risksense.restapi.assessment;

import io.vertx.core.Vertx;
import io.vertx.ext.unit.Async;
import io.vertx.ext.unit.TestContext;
import io.vertx.ext.unit.junit.VertxUnitRunner;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import java.io.IOException;
import java.net.ServerSocket;
import io.vertx.core.DeploymentOptions;
import io.vertx.core.json.JsonObject;

@RunWith(VertxUnitRunner.class)
public class JobSearchTest {

  private Vertx vertx;
  private Integer port;

  @Before
  public void setUp(TestContext context) throws IOException {
    vertx = Vertx.vertx();
    port = 8082;
    DeploymentOptions options = new DeploymentOptions().setConfig(new JsonObject().put("http.port", port)); 
    vertx.deployVerticle(JobSearch.class.getName(), context.asyncAssertSuccess());
  }

  @After
  public void tearDown(TestContext context) {
    vertx.close(context.asyncAssertSuccess());
  }

  @Test
  public void testJobSearch(TestContext context) {
    final Async async = context.async();

    vertx.createHttpClient().getNow(port, "localhost", "/",
     response -> {
      response.handler(body -> {
        context.assertTrue(body.toString().length() > 0);
        async.complete();
      });
    });
  }
}
