using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using System;
using UnityEngine.Networking;

public class CarSpawner : MonoBehaviour
{
    public int id = 0;
    
    public GameObject autoPrefab0;
    public GameObject autoPrefab1;

    IEnumerator Start()
    {
        InvokeRepeating("InstantiateCar", 1.0f, 1.0f);
        yield return new WaitForSeconds(300);       
    }

    void InstantiateCar(){

        // AgentController hinge = gameObject.GetComponent( typeof(AgentController) ) as AgentController;

                  
        GameObject CARRITO = Instantiate(autoPrefab0, new Vector3(0, 0.0f, 0), Quaternion.identity);

        CARRITO.GetComponent<AgentController>().unique_id = id;

        id++;
    }
       

}