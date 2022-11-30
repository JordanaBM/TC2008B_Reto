using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class CarData
{
    public string speed;
    public string unique_id;
    public string x;
    public string y;

    public static CarData CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<CarData>(jsonString);
    }
}