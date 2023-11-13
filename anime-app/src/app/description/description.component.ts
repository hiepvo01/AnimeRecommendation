import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {AlertService} from '@app/_services';
import { HttpClient } from '@angular/common/http';
import {environment} from '@environments/environment';

@Component({
  selector: 'app-description',
  templateUrl: './description.component.html',
  styleUrls: ['./description.component.less'],
})
export class DescriptionComponent implements OnInit {
  form: FormGroup;
  submitted = false;
  loading=false;

  constructor(
    private formBuilder: FormBuilder,
    private http: HttpClient,
  ) {}

  ngOnInit() {
    this.form = this.formBuilder.group({
      description: ['', Validators.required],
    });
  }

  // convenience getter for easy access to form fields
  get f() {
    return this.form.controls;
  }

  async onSubmit() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.form.invalid) {
      return;
    }

    // console.log(environment.apiUrl);
    // console.log(this.form.value);
    // this.http.post(`${environment.apiUrl}/description_rec`, this.form.value).subscribe(
    //   data => {console.log(data)});
    // const t = await this.http
    //   .get(`${environment.apiUrl}/des_res`, this.form.value)
  }
}
