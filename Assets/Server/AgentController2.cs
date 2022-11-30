using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
using System;
using UnityEditor;

public class AgentController2 : MonoBehaviour
{
    public Transform[] autosPrefabs;
    Vector3[] posAutos = new Vector3[25] { Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero, Vector3.zero };
    int[] contsPosAutos = new int[25] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    Transform[] Autos = new Transform[25];
    int clonesAuto = 1;
    float velocidad = 10.0f;
    private float timeToUpdate = 1.0f;
    private float timer;
    float dt;


    IEnumerator SendData(string data)
    {
        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585";
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            //www.SetRequestHeader("Content-Type", "text/html");
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                //Lista con todas las posiciones de los agentes
                //List<Vector3> newPositionsCar = new List<Vector3>();
                string txt = www.downloadHandler.text.Replace('\'', '\"');
                txt = txt.TrimStart('"', '{', 'd', 'a', 't', 'a', ':', '[');
                txt = "{\"" + txt;
                txt = txt.TrimEnd(']', '}');
                txt = txt + '}';
                string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
                for (int i = 0; i < strs.Length; i++)
                {
                    strs[i] = strs[i].Trim();

                    if (i == 0)
                    {
                        strs[i] = strs[i] + '}';
                        //print(strs[i]);
                    }
                    else if (i == strs.Length - 1)
                    {
                        strs[i] = '{' + strs[i];
                        //print(strs[i]);
                    }
                    else
                    {
                        strs[i] = '{' + strs[i] + '}';
                        //print(strs[i]);
                    }

                    Vector3 test = JsonUtility.FromJson<Vector3>(strs[i]);
                    //print(test.x + "," + test.y + "," + test.z);
                    int n = strs[i].Length;
                    int entero;
                    if (strs[i][n - 5] > 57 || strs[i][n - 5] < 48)
                    {
                        entero = strs[i][n - 4] - '0';
                    }
                    else
                    {
                        string indice = "";
                        indice = indice + strs[i][n - 5];
                        indice = indice + strs[i][n - 4];
                        entero = Int32.Parse(indice);
                    }

                    if (entero > 0 && entero < 60)
                    {

                        print("Auto numero " + entero);
                        clonesAuto++;
                        posAutos[entero] = test;
                        contsPosAutos[entero] = contsPosAutos[entero] + 1;
                    }
                  
                }

            }
        }

    }
    // Start is called before the first frame update
    void Start()
    {
        //Instanciar los autos
        for (int i = 1; i <= 20; i++)
        {
            Autos[i] = Instantiate(autosPrefabs[UnityEngine.Random.Range(0, 3)], posAutos[i], Quaternion.identity);
        }

#if UNITY_EDITOR
        Vector3 fakePos = new Vector3(clonesAuto, clonesAuto);
        string json = EditorJsonUtility.ToJson(fakePos);
        StartCoroutine(SendData(json));
        timer = timeToUpdate;
#endif

    }

    // Update is called once per frame
    void Update()
    {
        timer -= Time.deltaTime;
        dt = 1.0f - (timer / timeToUpdate);

        if (timer < 0)
        {
#if UNITY_EDITOR
            timer = timeToUpdate; // reset the timer
            //int autosActuales = clonesAuto++;
            Vector3 fakePos = new Vector3(clonesAuto, clonesAuto);
            string json = EditorJsonUtility.ToJson(fakePos);
            StartCoroutine(SendData(json));
#endif
        }

        //MOVEMOS LOS AUTOS
        for (int i = 1; i <= 20; i++)
        {
            if (contsPosAutos[i] > 1)
            {
                mover(Autos[i], posAutos[i], velocidad);
            }
            if (contsPosAutos[i] == 1)
            {
                Autos[i].transform.localPosition = posAutos[i];
            }
        }
    }

    Vector3 normalizar(Vector3 obj1)
    {
        obj1.x /= Mathf.Sqrt(Mathf.Pow(obj1.x, 2) + Mathf.Pow(obj1.y, 2) + Mathf.Pow(obj1.z, 2));
        obj1.y /= Mathf.Sqrt(Mathf.Pow(obj1.x, 2) + Mathf.Pow(obj1.y, 2) + Mathf.Pow(obj1.z, 2));
        obj1.z /= Mathf.Sqrt(Mathf.Pow(obj1.x, 2) + Mathf.Pow(obj1.y, 2) + Mathf.Pow(obj1.z, 2));
        return obj1;
    }
    void mover(Transform Object, Vector3 posFinal, float velocidad)
    {
        Vector3 direccion = normalizar(posFinal - Object.position);
        Object.position = Vector3.MoveTowards(Object.position, posFinal, Time.deltaTime * velocidad);
    }

    void mover2(Transform Object, Vector3 posFinal, float velocidad)
    {
        Object.LookAt(posFinal);
        Object.position += Object.forward * velocidad * Time.deltaTime;
    }
}