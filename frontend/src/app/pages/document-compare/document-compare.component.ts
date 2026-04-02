import { Component, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ComparisonResult, FileInfo, ContentBlock, ModifiedItem } from '../../models/comparison-result.model';

@Component({
  selector: 'app-document-compare',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './document-compare.component.html',
  styleUrls: ['./document-compare.component.css']
})
export class DocumentCompareComponent implements AfterViewInit {
  // File handling
  originalFile: FileInfo | null = null;
  revisedFile: FileInfo | null = null;

  // UI state
  isAnalyzing = false;
  activeTab: 'overview' | 'side-by-side' | 'added-removed' | 'full-content' = 'overview';
  showResults = false;

  // Analysis results
  comparisonResult: ComparisonResult | null = null;

  // File input references
  originalInput?: HTMLInputElement;
  revisedInput?: HTMLInputElement;

  // Drag and drop state
  isDragOverOriginal = false;
  isDragOverRevised = false;

  ngAfterViewInit(): void {
    // Set up file input references after view initialization
    setTimeout(() => {
      const originalElement = document.querySelector('#originalInput') as HTMLInputElement;
      const revisedElement = document.querySelector('#revisedInput') as HTMLInputElement;

      if (originalElement) {
        this.originalInput = originalElement;
      }
      if (revisedElement) {
        this.revisedInput = revisedElement;
      }
    });
  }

  onFileSelected(event: Event, type: 'original' | 'revised'): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) {
      this.setFile(file, type);
    }
  }

  onDragOver(event: DragEvent, type: 'original' | 'revised'): void {
    event.preventDefault();
    event.stopPropagation();
    if (type === 'original') {
      this.isDragOverOriginal = true;
    } else {
      this.isDragOverRevised = true;
    }
  }

  onDragLeave(event: DragEvent, type: 'original' | 'revised'): void {
    event.preventDefault();
    event.stopPropagation();
    if (type === 'original') {
      this.isDragOverOriginal = false;
    } else {
      this.isDragOverRevised = false;
    }
  }

  onDrop(event: DragEvent, type: 'original' | 'revised'): void {
    event.preventDefault();
    event.stopPropagation();

    if (type === 'original') {
      this.isDragOverOriginal = false;
    } else {
      this.isDragOverRevised = false;
    }

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.setFile(files[0], type);
    }
  }

  private setFile(file: File, type: 'original' | 'revised'): void {
    const fileInfo: FileInfo = {
      file,
      name: file.name,
      size: file.size,
      sizeFormatted: this.formatFileSize(file.size)
    };

    if (type === 'original') {
      this.originalFile = fileInfo;
    } else {
      this.revisedFile = fileInfo;
    }
  }

  removeFile(type: 'original' | 'revised'): void {
    if (type === 'original') {
      this.originalFile = null;
      if (this.originalInput) {
        this.originalInput.value = '';
      }
    } else {
      this.revisedFile = null;
      if (this.revisedInput) {
        this.revisedInput.value = '';
      }
    }
  }

  setFileInputRef(input: HTMLInputElement, type: 'original' | 'revised'): void {
    if (type === 'original') {
      this.originalInput = input;
    } else {
      this.revisedInput = input;
    }
  }

  canAnalyze(): boolean {
    return !!(this.originalFile && this.revisedFile && !this.isAnalyzing);
  }

  async runAnalysis(): Promise<void> {
    if (!this.canAnalyze()) {
      return;
    }

    this.isAnalyzing = true;
    this.showResults = false;

    // Simulate analysis delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Generate mock results
    this.comparisonResult = this.generateMockResults();
    this.showResults = true;
    this.isAnalyzing = false;
  }

  setActiveTab(tab: 'overview' | 'side-by-side' | 'added-removed' | 'full-content'): void {
    this.activeTab = tab;
  }

  private generateMockResults(): ComparisonResult {
    const originalContent = `This is the original document content.
It contains several paragraphs of text.
Some content will be modified in the revised version.
This line remains unchanged.
The original document has specific formatting and content.`;

    const revisedContent = `This is the revised document content.
It contains several paragraphs of text with some changes.
Some content has been modified in the revised version.
This line has been updated with new information.
The revised document has different formatting and additional content.`;

    return {
      totalDifferences: 8,
      addedCount: 3,
      removedCount: 2,
      modifiedCount: 3,
      similarityScore: 78,
      originalContentBlocks: this.parseContentBlocks(originalContent, 'original'),
      revisedContentBlocks: this.parseContentBlocks(revisedContent, 'revised'),
      addedItems: [
        'additional content',
        'new information',
        'different formatting'
      ],
      removedItems: [
        'specific formatting',
        'original document has'
      ],
      modifiedItems: [
        {
          original: 'Some content will be modified in the revised version',
          revised: 'Some content has been modified in the revised version',
          lineNumber: 3
        },
        {
          original: 'This line remains unchanged',
          revised: 'This line has been updated with new information',
          lineNumber: 4
        },
        {
          original: 'The original document has specific formatting and content',
          revised: 'The revised document has different formatting and additional content',
          lineNumber: 5
        }
      ]
    };
  }

  private parseContentBlocks(content: string, type: 'original' | 'revised'): ContentBlock[] {
    const lines = content.split('\n');
    return lines.map((line, index) => ({
      id: `${type}-${index}`,
      type: this.getBlockType(line, index, type),
      content: line,
      lineNumber: index + 1
    }));
  }

  private getBlockType(line: string, index: number, type: 'original' | 'revised'): ContentBlock['type'] {
    // Mock logic for determining block types
    const mockChanges = {
      2: 'modified',
      3: 'modified',
      4: 'modified'
    };

    if (mockChanges[index as keyof typeof mockChanges]) {
      return mockChanges[index as keyof typeof mockChanges] as ContentBlock['type'];
    }

    if (type === 'original' && (index === 0 || index === 1)) {
      return 'unchanged';
    }

    if (type === 'revised' && index === 0) {
      return 'added';
    }

    return 'unchanged';
  }

  private formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  getChangeClass(type: ContentBlock['type']): string {
    switch (type) {
      case 'added': return 'change-added';
      case 'removed': return 'change-removed';
      case 'modified': return 'change-modified';
      default: return '';
    }
  }

  getSummaryIcon(type: 'total' | 'added' | 'removed' | 'modified' | 'similarity'): string {
    switch (type) {
      case 'total': return '📊';
      case 'added': return '➕';
      case 'removed': return '➖';
      case 'modified': return '✏️';
      case 'similarity': return '📈';
      default: return '';
    }
  }

  getSummaryColor(type: 'total' | 'added' | 'removed' | 'modified' | 'similarity'): string {
    switch (type) {
      case 'added': return '#d4edda';
      case 'removed': return '#f8d7da';
      case 'modified': return '#fff3cd';
      case 'similarity': return '#d1ecf1';
      default: return '#f8f9fa';
    }
  }
}