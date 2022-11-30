// TC2008B Modelaci�n de Sistemas Multiagentes con gr�ficas computacionales
// C# client to interact with Python server via POST
// Sergio Ruiz-Loza, Ph.D. March 2021

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.Networking;


public class WebClient : MonoBehaviour
{
    // Start is called before the first frame update
    IEnumerator Start()
    {
        Invoke("GetData", 0.3f);
        InvokeRepeating("GetData", 0.0f, 1.0f);
        yield return new WaitForSeconds(300);
        CancelInvoke("GetData");
  
    }
    
    void GetData ()
    {
        StartCoroutine(GetDataCoroutine());
    }
    
    IEnumerator GetDataCoroutine(){
        // Wait 5 seconds before doing a request
        string url = "http://localhost:5000/step";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            // Wait 1 second
            yield return www.SendWebRequest();
            if(www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
                // text.text = www.error;
            }
            else
            {
                Debug.Log(www.downloadHandler.text);
                // text.text = www.downloadHandler.text;
            }
        }
    }
 
}