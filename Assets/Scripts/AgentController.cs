using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.Networking;


public class AgentController : MonoBehaviour
{
   public int unique_id;
   public string position;
   private int modifiedZ;

    IEnumerator Start()
    {
        InvokeRepeating("GetData", 0.0f, 1.01f);
        yield return new WaitForSeconds(300);
        CancelInvoke("GetData");  
    }

    void GetData ()
    {
        StartCoroutine(GetDataCoroutine());
    }
    
    //Corrutina que se manda a llamar cada segundo para obtener las posiciones
    // de los objetos carro que tienen id
    IEnumerator GetDataCoroutine(){
        string url = "http://localhost:5000/position?id=" + unique_id;
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            yield return www.SendWebRequest();
            if(www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
                position = www.error;  

            }
            else
            {
                //Descomponemos la respuesta del servidor
                position= www.downloadHandler.text;
                position = position.TrimStart('[');
                position = position.TrimEnd(']');
                
                string[] positionArray = position.Split(',');
                string x = positionArray[0];
                x= x.TrimStart('{', '"', 'x', '"', ':');
                x= x.TrimEnd(' ');
                //Para que al final solo nos quede un número entero
                // y podemos crear un vector
                int positionX = int.Parse(x);

                //Si la posición en x es 1, es porque va en el carril del centro
                if (positionX == 1){
                    //En unity es el carril con ubicación en -3
                    positionX = -3;
                }
                // Si la posición en x es 2 es porque va en el carril de la izquierda
                else if(positionX == 2){
                    //En unity es el carril con ubicación en -6
                    positionX = -6;
                }
                // Si la x es 0, es porque va en el carril de la derecha, lo mismo en unity

                string z = positionArray[2];
                z= z.TrimStart(' ','"', 'z', '"', ':');
                z= z.TrimEnd(' ');
                int positionZ = int.Parse(z);


                //La posición se multiplica por 5, debido a que nuestro carro mide
                // 5 posiciones en unity
                positionZ = positionZ * 5;
                        

                Vector3 currentPosition = transform.position;
                Vector3 targetPos = new Vector3(positionX , 0.0f, positionZ);

                float timeElapsed = 0;
                float timeToMove = 1f;

                if (unique_id != 30){
                    Destroy(gameObject,60);
                }

                while (timeElapsed < timeToMove)
                {
                    //Movemos nuestro carro a la nuea posición
                    transform.position = Vector3.Lerp(currentPosition, targetPos, timeElapsed / timeToMove);
                    timeElapsed += Time.deltaTime;
                    yield return null;
                }

            }
        }
    }
}