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
    // Invocamos el get data cada segundo
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

        //Cada segundo estará realizando un step de la simulación
        string url = "http://localhost:5000/step";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            yield return www.SendWebRequest();
            if(www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                //Aquí está el print de como llegan todas nuestras posiciones
                //Debug.Log(www.downloadHandler.text);
            }
        }
    }
 
}