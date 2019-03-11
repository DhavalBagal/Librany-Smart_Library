package com.example.dhavalbagal.libranyrc;

import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.support.annotation.NonNull;
import android.support.constraint.ConstraintLayout;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputType;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.json.JSONException;
import org.json.JSONObject;

public class Dashboard extends AppCompatActivity {

    Button issuebutton, returnbutton, searchbutton;
    RequestQueue queue;
    JsonObjectRequest req1, req2, req3;
    JSONObject postparams1,postparams2, postparams3;
    String issueurl, returnurl,searchurl, url, u;
    DatabaseReference urlref;

    ProgressDialog p;

    public Dashboard()
    {

    }

    protected void initurl(String s)
    {
        url = s;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        p = new ProgressDialog(Dashboard.this);
        p.setMessage("Fetching URL of the server...");
        p.show();

        urlref = FirebaseDatabase.getInstance().getReference("URL");

        urlref.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                u = dataSnapshot.getValue(String.class);
                Log.v("msg",u);
                initurl(u);
                p.dismiss();
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        url = "http://192.168.43.15:5000";
        /*Initializing all variables*/
        issuebutton = findViewById(R.id.issuebutton);
        returnbutton = findViewById(R.id.returnbutton);
        searchbutton = findViewById(R.id.searchbutton);


        /*Creating a request queue*/
        queue = Volley.newRequestQueue(Dashboard.this);

        /*Creating a json object in which data is fed and sent to the server*/
        postparams1 = new JSONObject();
        postparams2 = new JSONObject();
        postparams3 = new JSONObject();


        issuebutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                issueurl = url+"/issuebook";

                /*Creating requests to send*/

                try
                {
                    postparams1.put("command", "ISSUE");

                    /*Creating a json object request in which the json object is put*/
                    /*Also adding response listener and response listener upon error*/

                    req1 = new JsonObjectRequest(issueurl, postparams1, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            enableButtons();

                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {

                        }
                    });

                    /*Setting retry policy to avoid sending data twice through volley*/
                    req1.setRetryPolicy(new DefaultRetryPolicy(
                            0,
                            DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                            DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                queue.add(req1);
                disableButtons();
            }
        });

        returnbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                returnurl = url+"/returnbook";

                try
                {
                    postparams2.put("command", "RETURN");

                    /*Creating a json object request in which the json object is put*/
                    /*Also adding response listener and response listener upon error*/

                    req2 = new JsonObjectRequest(returnurl, postparams2, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            enableButtons();

                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {

                        }
                    });

                    /*Setting retry policy to avoid sending data twice through volley*/
                    req2.setRetryPolicy(new DefaultRetryPolicy(
                            0,
                            DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                            DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                queue.add(req2);
                disableButtons();
            }
        });

        searchbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                searchurl = url+"/searchbook";

                try
                {
                    postparams3.put("command", "SEARCH");

                    /*Creating a json object request in which the json object is put*/
                    /*Also adding response listener and response listener upon error*/

                    req3 = new JsonObjectRequest(searchurl, postparams3, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            enableButtons();

                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {

                        }
                    });

                    /*Setting retry policy to avoid sending data twice through volley*/
                    req3.setRetryPolicy(new DefaultRetryPolicy(
                            0,
                            DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                            DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                } catch (JSONException e) {
                    e.printStackTrace();
                }


                queue.add(req3);
                disableButtons();
            }
        });



    }

    protected void disableButtons()
    {
        issuebutton.setEnabled(false);
        returnbutton.setEnabled(false);
        searchbutton.setEnabled(false);
    }

    protected void enableButtons()
    {
        issuebutton.setEnabled(true);
        returnbutton.setEnabled(true);
        searchbutton.setEnabled(true);
    }


}
