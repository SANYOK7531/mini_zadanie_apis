using cvicenie_mvc.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using Microsoft.Data.SqlClient;
using System.Net.Http.Headers;

namespace cvicenie_mvc.Controllers
{
    public class StudentController : Controller
    {
        private readonly Repository repository = new Repository();
        public IActionResult Read()
        {
            return View(repository.GetAllStudents());
        }

        public async Task<IActionResult> Index_json()
        {
            //var baseUrl = "http://127.0.0.1:5000";
            var baseUrl = "https://msdocs-python-webapp-quickstart-petsa-hpfwfvcshafhbhe3.francecentral-01.azurewebsites.net/Students";


            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(baseUrl);
                client.DefaultRequestHeaders.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                HttpResponseMessage getData = await client.GetAsync("Students");

                if (getData.IsSuccessStatusCode)
                {
                    return View(repository.GetAllStudentsFromJson(getData));
                }
                else
                {
                    throw new HttpRequestException($"Failed to fetch data. Status code: {getData.StatusCode}");
                }
            }
        }
        
        public async Task<IActionResult> Prediction(int studentId)
        {
            //var baseUrl = "http://127.0.0.1:5000";
            var baseUrl = "https://msdocs-python-webapp-quickstart-petsa-hpfwfvcshafhbhe3.francecentral-01.azurewebsites.net/Students";


            StudentModel student = repository.GetJsonStudent(studentId);

            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(baseUrl);
                client.DefaultRequestHeaders.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                HttpResponseMessage getData = await client.GetAsync("Predict?Scores=" + student.Scores);

                if (getData.IsSuccessStatusCode)
                {
                    ViewBag.Message = repository.Prediction(getData);
                    return View(student);
                }
                else
                {
                    throw new HttpRequestException($"Failed to fetch data. Status code: {getData.StatusCode}");
                }
            }
        }
        
        public IActionResult Student_info(string name, int age, int id = 1)
        {

            StudentModel student = new StudentModel();
            student.Id = id;
            student.Name = name;
            student.Gender = "Male";
            student.City = "Kosice";
            student.Age = age;

            return View(student);
        }

        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Create(StudentModel studentModel)
        {
            repository.Create(studentModel);
            return View("Thanks", studentModel);
        }

        public IActionResult Update(int studentId)
        {
            StudentModel student = repository.GetAllStudents().Where(e => e.Id == studentId).First();
            return View(student);
        }

        [HttpPost]
        public IActionResult Update(StudentModel student, int studentId)
        {
            repository.Update(student, studentId);
            return RedirectToAction("Read");
        }

        [HttpPost]
        public IActionResult Delete(int studentId)
        {
            repository.Delete(studentId);
            return RedirectToAction("Read");
        }
    }
}
