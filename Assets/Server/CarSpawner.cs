using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using System;
using UnityEngine.Networking;

public class CarSpawner : MonoBehaviour
{
    public int unique_id = 0;
    
    public GameObject autoPrefab0;
    public GameObject autoPrefab1;

    IEnumerator Start()
    {
        InvokeRepeating("InstantiateCar", 1.0f, 1.6f);
        yield return new WaitForSeconds(100);       
    }

    void InstantiateCar(){

        int carros = UnityEngine.Random.Range(0, 1);
        if (carros == 0){
            autoPrefab0.GetComponent<AgentController>().unique_id = unique_id;
            unique_id++;
            Instantiate(autoPrefab0, new Vector3(0, 0, 0), Quaternion.identity);
        }

        else if (carros == 1){
            autoPrefab1.GetComponent<AgentController>().unique_id = unique_id;
            unique_id++;
            Instantiate(autoPrefab1, new Vector3(-3, 0, 0), Quaternion.identity);
        }

    }

}