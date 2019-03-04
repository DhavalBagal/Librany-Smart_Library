package com.example.dhavalbagal.libranyrc;

import android.app.ProgressDialog;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
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
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Catalogue extends AppCompatActivity {

    EditText titletxt, authortxt, editiontxt, keywordstxt;
    Button gobutton;
    String title;
    String author;
    String edition;
    String keywords;

    FirebaseAuth mAuth;

    Long c;

    DatabaseReference countref, booksref;

    RequestQueue queue;
    JsonObjectRequest req;
    JSONObject postparams;
    String catalogueurl, url;

    ProgressDialog p;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_catalogue);

        /*Initialization*/
        titletxt = findViewById(R.id.titletext);
        authortxt = findViewById(R.id.authortext);
        editiontxt = findViewById(R.id.editiontext);
        keywordstxt = findViewById(R.id.keywordstext);
        gobutton = findViewById(R.id.gobutton);

        p = new ProgressDialog(Catalogue.this);

        url="http://192.168.0.101:5000";
        catalogueurl = url+"/cataloguebook";

        queue = Volley.newRequestQueue(Catalogue.this);
        postparams = new JSONObject();

        /*Intializing firebase related stuff*/

        mAuth = FirebaseAuth.getInstance();
        mAuth.signInWithEmailAndPassword("dhavalbagal99@gmail.com", "Dhaval123");

        gobutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                p.setMessage("Adding book...");
                p.show();

                title = titletxt.getText().toString();
                author = authortxt.getText().toString();
                edition = editiontxt.getText().toString();
                keywords = keywordstxt.getText().toString();

                if (title.trim().equals(""))
                {
                    Toast.makeText(Catalogue.this, "Title of the book cannot be empty!",Toast.LENGTH_LONG).show();
                }
                else if (author.trim().equals(""))
                {
                    Toast.makeText(Catalogue.this, "Author of the book cannot be empty!",Toast.LENGTH_LONG).show();
                }

                countref = FirebaseDatabase.getInstance().getReference("COUNT");
                booksref = FirebaseDatabase.getInstance().getReference("BOOKS");

                countref.addListenerForSingleValueEvent(new ValueEventListener() {
                    @Override
                    public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                        c = (Long) dataSnapshot.child("Books").getValue();
                        Map<String,Long> count = new HashMap<>();
                        count.put("Books", (c+1));
                        countref.setValue(count);

                        booksref.addListenerForSingleValueEvent(new ValueEventListener() {
                            @Override
                            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                                String key = "B"+(c+1);
                                Map<String,String> bk = new HashMap<>();
                                bk.put("Author",author);
                                bk.put("Availability", "Available");
                                bk.put("Issued_By"," ");
                                bk.put("Title",title);

                                if (!keywords.trim().equals(""))
                                    bk.put("Keywords",keywords);
                                bk.put("Edition",edition);

                                booksref.child(key).setValue(bk);

                                try
                                {
                                    postparams.put("command", "CATALOGUE");
                                    postparams.put("data", key);

                                    /*Creating a json object request in which the json object is put*/
                                    /*Also adding response listener and response listener upon error*/

                                    req = new JsonObjectRequest(catalogueurl, postparams, new Response.Listener<JSONObject>() {
                                        @Override
                                        public void onResponse(JSONObject response) {
                                            p.dismiss();
                                            Toast.makeText(Catalogue.this, "Book added successfully!",Toast.LENGTH_LONG).show();
                                            startActivity(new Intent(Catalogue.this, Dashboard.class));
                                        }
                                    }, new Response.ErrorListener() {
                                        @Override
                                        public void onErrorResponse(VolleyError error) {

                                        }
                                    });

                                    /*Setting retry policy to avoid sending data twice through volley*/
                                    req.setRetryPolicy(new DefaultRetryPolicy(
                                            0,
                                            DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                                            DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                                    queue.add(req);

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                            }

                            @Override
                            public void onCancelled(@NonNull DatabaseError databaseError) {

                            }
                        });
                    }

                    @Override
                    public void onCancelled(@NonNull DatabaseError databaseError) {

                    }
                });



            }
        });

    }
}
