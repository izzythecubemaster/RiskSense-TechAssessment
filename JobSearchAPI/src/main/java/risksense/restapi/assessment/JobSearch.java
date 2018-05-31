package risksense.restapi.assessment;

import io.vertx.core.AbstractVerticle;
import io.vertx.core.Future;
import io.vertx.core.http.HttpServerResponse;
import io.vertx.core.json.Json;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.Router;
import io.vertx.ext.web.RoutingContext;
import io.vertx.ext.web.handler.BodyHandler;
import io.vertx.ext.web.handler.StaticHandler;

import java.util.LinkedHashMap;
import java.util.Map;

public class JobSearch extends AbstractVerticle {

  @Override
  public void start(Future<Void> fut) {
    Router router = Router.router(vertx);
    router.route("/").handler(routingContext -> {
      HttpServerResponse response = routingContext.response();
      response
  	.putHeader("content-type","text/html")
  	.end("<h1>Result will go here.</h1>");
    });
    router.route("/assets/*").handler(StaticHandler.create("assets"));
    vertx
      .createHttpServer()
      .requestHandler(router::accept)
      .listen(config().getInteger("http.port",8082), result -> {
        if (result.succeeded()) {
          fut.complete();
        } else {
          fut.fail(result.cause());
        }
      });
  }
}
