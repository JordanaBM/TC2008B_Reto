using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DestroyCar : MonoBehaviour
{
   

    void Start()
    {
      
    }
    // Update is called once per frame
    void Update()
    {
        //Se destuye un carro después de 2 minutos
        if (this.unique_id != 30){
            Destroy(gameObject,120);
        }
    }

}