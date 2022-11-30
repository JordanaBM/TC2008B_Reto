using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[System.Serializable]
public class JSONParser : MonoBehaviour
{
    public CarData data;
    
    void Start()
    {
       data = CarData.CreateFromJSON("http://127.0.0.1:5000/step");
    }

    
}
