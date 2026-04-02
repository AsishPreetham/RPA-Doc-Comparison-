import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UploadResponse {
  message: string;
  document_a: string;
  document_b: string;
  document_a_preview: string;
  document_b_preview: string;
}

export interface ComparisonResult {
  comparison_id: string;
  message: string;
  result: ComparisonData[];
}

export interface ComparisonData {
  type: 'added' | 'removed' | 'modified' | 'same';
  text: string;
  section?: string;
  line_number?: number;
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private apiUrl = 'http://localhost:8000'; // Adjust based on your backend URL

  constructor(private http: HttpClient) {}

  uploadDocuments(fileA: File, fileB: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('document_a', fileA);
    formData.append('document_b', fileB);

    return this.http.post<UploadResponse>(`${this.apiUrl}/upload`, formData);
  }

  compareDocuments(): Observable<ComparisonResult> {
    return this.http.post<ComparisonResult>(`${this.apiUrl}/compare`, {});
  }
}