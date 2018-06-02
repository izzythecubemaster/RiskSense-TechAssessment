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

import java.io.StringWriter;
import java.io.PrintWriter;
import java.util.LinkedHashMap;
import java.util.Map;

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

public class JobSearch extends AbstractVerticle {
  Connection conn = null;
  Statement stmt = null;
  ResultSet rs = null;

  @Override
  public void start(Future<Void> fut) {
    Router router = Router.router(vertx);
    router.route("/").handler(routingContext -> {
      HttpServerResponse response = routingContext.response();
      response
        .putHeader("content-type","application/json; charset=utf8")
        .end(GetDataAsJSON());
    });
    router.route("/assets/*").handler(StaticHandler.create("assets"));
    vertx
      .createHttpServer()
      .requestHandler(router::accept)
      .listen(config().getInteger("http.port",80), result -> {
        if (result.succeeded()) {
          fut.complete();
        } else {
          fut.fail(result.cause());
        }
      });
  }

  private String GetDataAsJSON() {
    try {
      conn = DriverManager.getConnection("jdbc:mysql://localhost/job_listing_data?user=rs_admin&password=risksense");
      stmt = conn.createStatement();
      rs = stmt.executeQuery("SELECT * FROM job_listings");
      if (stmt.execute("SELECT * FROM job_listings;")){
	rs = stmt.getResultSet();
      }
      return convertToJSON(rs).toString();
    }
    catch (SQLException ex){
      String exceptionString = "SQLException: "+ex.getMessage()
	+ "\nSQLState: "+ex.getSQLState()
	+ "\nVendorError: "+ex.getErrorCode();
      return exceptionString;
    }
    finally {
      if (rs != null){
	try {
	  rs.close();
	}
	catch (SQLException sqlEx){}
	rs = null; 
      }
      if (stmt != null){
	try {
	  stmt.close();
	}
	catch (SQLException sqlEx){}
	stmt = null;
      }
    }
  }

  private static JSONArray convertToJSON( ResultSet rs )
    throws SQLException, JSONException
      {
        JSONArray json = new JSONArray();
        ResultSetMetaData rsmd = rs.getMetaData();

        while(rs.next()) {
          int numColumns = rsmd.getColumnCount();
          JSONObject obj = new JSONObject();

          for (int i=1; i<numColumns+1; i++) {
            String column_name = rsmd.getColumnName(i);

            if(rsmd.getColumnType(i)==java.sql.Types.ARRAY){
              obj.put(column_name, rs.getArray(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.BIGINT){
              obj.put(column_name, rs.getInt(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.BOOLEAN){
              obj.put(column_name, rs.getBoolean(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.BLOB){
              obj.put(column_name, rs.getBlob(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.DOUBLE){
              obj.put(column_name, rs.getDouble(column_name)); 
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.FLOAT){
              obj.put(column_name, rs.getFloat(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.INTEGER){
              obj.put(column_name, rs.getInt(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.NVARCHAR){
              obj.put(column_name, rs.getNString(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.VARCHAR){
              obj.put(column_name, rs.getString(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.TINYINT){
              obj.put(column_name, rs.getInt(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.SMALLINT){
              obj.put(column_name, rs.getInt(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.DATE){
              obj.put(column_name, rs.getDate(column_name));
            }
            else if(rsmd.getColumnType(i)==java.sql.Types.TIMESTAMP){
              obj.put(column_name, rs.getTimestamp(column_name));   
            }
            else{
              obj.put(column_name, rs.getObject(column_name));
            }
          }
        json.put(obj);
      }
    return json;
  }
}
