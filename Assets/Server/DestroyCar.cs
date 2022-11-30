using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DestroyCar : MonoBehaviour
{
    Camera camera;
    MeshRenderer renderer;
    Plane[] cameraFrustum;
    Collider collider;


    void Start()
    {
        camera = Camera.main;
        renderer = GetComponent<MeshRenderer>();
        collider = GetComponent<Collider>();
    }

    // Update is called once per frame

    void Update()
    {
     

        var bounds = collider.bounds;
        cameraFrustum = GeometryUtility.CalculateFrustumPlanes(camera);
        if (GeometryUtility.TestPlanesAABB(cameraFrustum, bounds))
        {
            var i = 0;
        }
        else
        {
            DestroyGameObject();
        }

       
    }

    void DestroyGameObject()
    {
        Destroy(gameObject);
    }
}