package com.example.dhavalbagal.libranyrc;

import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
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

import org.json.JSONException;
import org.json.JSONObject;

public class Dashboard extends AppCompatActivity {

    Button issuebutton, returnbutton, searchbutton, cataloguebutton;
    RequestQueue queue;
    JsonObjectRequest req1, req2, req3;
    JSONObject postparams1,postparams2, postparams3;
    String issueurl, returnurl,searchurl, url;
    String m_Text;

    ProgressDialog p;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        /*Initializing all variables*/
        issuebutton = findViewById(R.id.issuebutton);
        returnbutton = findViewById(R.id.returnbutton);
        searchbutton = findViewById(R.id.searchbutton);
        cataloguebutton = findViewById(R.id.cataloguebutton);

        p = new ProgressDialog(Dashboard.this);

        /*Initializing the urls*/
        url="http://192.168.0.101:5000";
        issueurl = url+"/issuebook";
        returnurl = url+"/returnbook";
        searchurl = url+"/searchbook";

        /*Creating a request queue*/
        queue = Volley.newRequestQueue(Dashboard.this);

        /*Creating a json object in which data is fed and sent to the server*/
        postparams1 = new JSONObject();
        postparams2 = new JSONObject();
        postparams3 = new JSONObject();

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


        issuebutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                queue.add(req1);
                disableButtons();
            }
        });

        returnbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                queue.add(req2);
                disableButtons();
            }
        });

        searchbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                m_Text="";

                LayoutInflater li = LayoutInflater.from(Dashboard.this);
                View promptsView = li.inflate(R.layout.prompts, null);

                AlertDialog.Builder builder = new AlertDialog.Builder(Dashboard.this);

                builder.setView(promptsView);

                final EditText userInput = (EditText) promptsView
                        .findViewById(R.id.prompttxt);

                Button ok = (Button) promptsView.findViewById(R.id.ok);

                Button cancel = (Button) promptsView.findViewById(R.id.cancel);

                final AlertDialog alertDialog = builder.create();
                alertDialog.show();

                ok.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        m_Text = userInput.getText().toString();
                        alertDialog.dismiss();
                        p.setMessage("Searching...");
                        p.show();

                        try
                        {
                            postparams3.put("command", "SEARCH");
                            postparams3.put("bookid",m_Text);

                            //*Creating a json object request in which the json object is put*//*
                            //*Also adding response listener and response listener upon error*//*

                            req3 = new JsonObjectRequest(searchurl, postparams3, new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    try {
                                        String rspns = response.getString("response");
                                        alertDialog.dismiss();
                                        p.dismiss();

                                        Toast.makeText(Dashboard.this, rspns, Toast.LENGTH_LONG).show();

                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }


                                }
                            }, new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {

                                }
                            });

                            //*Setting retry policy to avoid sending data twice through volley*//*
                            req3.setRetryPolicy(new DefaultRetryPolicy(
                                    0,
                                    DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                            queue.add(req3);

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                });

                cancel.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        alertDialog.dismiss();
                    }
                });




                /*builder.setTitle("Enter the book code");

                // Set up the input
                final EditText input = new EditText(Dashboard.this);

                input.setLayoutParams(new ConstraintLayout.LayoutParams(ConstraintLayout.LayoutParams.FILL_PARENT,20));

                // Specify the type of input expected; this, for example, sets the input as a password, and will mask the text
                input.setInputType(InputType.TYPE_CLASS_TEXT );

                builder.setView(input);

                // Set up the buttons
                builder.setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(final DialogInterface dialog, int which) {
                        m_Text = input.getText().toString();

                        try
                        {
                            postparams3.put("command", "SEARCH");
                            postparams3.put("bookid",m_Text);

                            *//*Creating a json object request in which the json object is put*//*
                            *//*Also adding response listener and response listener upon error*//*

                            req3 = new JsonObjectRequest(searchurl, postparams3, new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    try {
                                        String rspns = response.getString("response");
                                        dialog.cancel();
                                        p.dismiss();

                                        Toast.makeText(Dashboard.this, rspns, Toast.LENGTH_LONG).show();

                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }


                                }
                            }, new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {

                                }
                            });

                            *//*Setting retry policy to avoid sending data twice through volley*//*
                            req3.setRetryPolicy(new DefaultRetryPolicy(
                                    0,
                                    DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                            queue.add(req3);

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                });
                builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });

                builder.show();*/

            }
        });

        cataloguebutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Dashboard.this, Catalogue.class));
            }
        });
    }

    protected void disableButtons()
    {
        issuebutton.setEnabled(false);
        returnbutton.setEnabled(false);
        searchbutton.setEnabled(false);
        cataloguebutton.setEnabled(false);
    }

    protected void enableButtons()
    {
        issuebutton.setEnabled(true);
        returnbutton.setEnabled(true);
        searchbutton.setEnabled(true);
        cataloguebutton.setEnabled(true);
    }


}
