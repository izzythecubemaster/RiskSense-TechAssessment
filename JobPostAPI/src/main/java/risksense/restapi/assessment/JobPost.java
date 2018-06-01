package risksense.restapi.assessment;

// Vert.x
import io.vertx.core.AbstractVerticle;
import io.vertx.core.Future;
import io.vertx.core.http.HttpServerResponse;
import io.vertx.core.json.Json;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.Router;
import io.vertx.ext.web.RoutingContext;
import io.vertx.ext.web.handler.BodyHandler;
import io.vertx.ext.web.handler.StaticHandler;

// MySQL Driver
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;

// For JSON conversion
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONException;

// Kafka
import java.util.Properties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.Producer;

public class JobPost extends AbstractVerticle {

  @Override
  public void start(Future<Void> fut) {
    Router router = Router.router(vertx);
    router.route().handler(BodyHandler.create());
    router.post("/").handler(this::addJob);
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
  private void addJob(RoutingContext routingContext){
    // Get job listing data in JSON format from POST
    JSONArray postData = new JSONArray(routingContext.getBodyAsString());

    // Kafka producer settings
    String topicName = "job_listings";
    Properties props = new Properties();
    props.put("bootstrap.servers","localhost:9092");
    props.put("acks","0");
    props.put("retries",0);
    props.put("batch.size", 100000);
    props.put("linger.ms", 1);
    props.put("buffer.memory", 1572864);
    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
    Producer<String, String> producer = new KafkaProducer<String, String>(props);    

    Integer listingsSent = 0;

    // Iterate through job listing array and send the listing in JSON format to the Kafka server's queue
    for(int i = 0; i < postData.length(); i++)
    {
      JSONObject jobListing = postData.getJSONObject(i);
      String jobString = jobListing.toString();
      producer.send(new ProducerRecord<String, String>(topicName, "json_listing_"+jobString.hashCode(),jobString));
      listingsSent++;
      producer.close();
    }
    String responseString;
    if (listingsSent == 1){
      responseString = "<h1>"+listingsSent+" Job listing has been added to the Kafka queue.</h1>";
    }
    else {
      responseString = "<h1>"+listingsSent+" Job listings have been added to the Kafka queue.</h1>";
    }
    routingContext.response()
      .setStatusCode(201)
      .putHeader("content-type","text/html")
      .end(responseString);
  }
}
