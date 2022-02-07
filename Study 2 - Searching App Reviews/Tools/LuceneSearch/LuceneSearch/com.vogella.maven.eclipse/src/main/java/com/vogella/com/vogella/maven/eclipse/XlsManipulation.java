package com.vogella.com.vogella.maven.eclipse;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import org.apache.poi.EncryptedDocumentException;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.apache.poi.ss.usermodel.CellType;

/**
 * @author jacekdabrowski
 * Class for manipulating excel files, including:
 * creating, reading, writing and editing file
 * the file will serve to store reviews for later annotation
 * 
 */


public class XlsManipulation {
	
	private Object getCellValue(Cell cell) {
	    switch (cell.getCellTypeEnum()) {
	    
	    case STRING:
	        return cell.getStringCellValue();
	 
	    case BOOLEAN:
	        return cell.getBooleanCellValue();
	 
	    case NUMERIC:
	        return cell.getNumericCellValue();
	    }
	 
	    return null;
	}
	
	// Read xls file with app reviews
	public List<Review> readFile(String pathname, String filename, int numberReviews) {
		try{
			
			String excelFilePath = pathname + filename;
			
			List<Review> listAppReviews = new ArrayList<>();

			FileInputStream inputStream = new FileInputStream(new File(excelFilePath));
			Workbook workbook = new XSSFWorkbook(inputStream);
			Sheet SheetReviews = workbook.getSheet("Reviews");
			
			Iterator<Row> iterator = SheetReviews.iterator();

			// Skip the head row
			if (iterator.hasNext())
				iterator.next();
			
			int currentRow = 0;
			
			while (iterator.hasNext() & currentRow < numberReviews) {
				
				currentRow += 1;
				Row nextRow = iterator.next();
				Iterator<Cell> cellIterator = nextRow.cellIterator();
				
				Review AppReview = new Review();
				
				while (cellIterator.hasNext()) {
					Cell nextCell = cellIterator.next();
					int columnIndex = nextCell.getColumnIndex();
					
					switch (columnIndex) {
						case 0:
								AppReview.setAppId((String) getCellValue(nextCell));
								break;
						case 1:
								AppReview.setReviewId((String) getCellValue(nextCell));
								break;
						case 2:
								AppReview.setContent((String) getCellValue(nextCell));
								break;
						default:
							break;
												
						}
				}
				
				listAppReviews.add(AppReview);
			}
			
			workbook.close();
			inputStream.close();
			
		return listAppReviews;
			
		}
		catch(Exception e){
			
			System.err.println("Colleciton of App Reviews could not be returned.");
			return null;
		}
			
	}
	
	// Create an xls file at specific location to store searching results from Lucene
	public boolean CreateFile(String pathname, String filename){
		try{
			
			Workbook workbook = new XSSFWorkbook();
			Sheet sheet = workbook.createSheet("Results");
			
			sheet.setColumnWidth(0, 7000);
			sheet.setColumnWidth(1, 7000);
			sheet.setColumnWidth(2, 7000);
			sheet.setColumnWidth(3, 9000);
			sheet.setColumnWidth(4, 9000);
			sheet.setColumnWidth(5, 7000);
			
			Row header = sheet.createRow(0);
			 
			CellStyle headerStyle = workbook.createCellStyle();
			headerStyle.setFillForegroundColor(IndexedColors.LIGHT_BLUE.getIndex());
			headerStyle.setFillPattern(FillPatternType.SOLID_FOREGROUND);
			 
			XSSFFont font = ((XSSFWorkbook) workbook).createFont();
			font.setFontName("Arial");
			font.setFontHeightInPoints((short) 16);
			font.setBold(true);
			headerStyle.setFont(font);
			 
			Cell headerCell;
			
			headerCell = header.createCell(0);
			headerCell.setCellValue("App id");
			headerCell.setCellStyle(headerStyle);

			headerCell = header.createCell(1);
			headerCell.setCellValue("Review id");
			headerCell.setCellStyle(headerStyle);
			
			headerCell = header.createCell(2);
			headerCell.setCellValue("Review content");
			headerCell.setCellStyle(headerStyle);
			
			headerCell = header.createCell(3);
			headerCell.setCellValue("Query (Orginal)");
			headerCell.setCellStyle(headerStyle);
			
			headerCell = header.createCell(4);
			headerCell.setCellValue("Query (Preprocessed)");
			headerCell.setCellStyle(headerStyle);
			
			headerCell = header.createCell(5);
			headerCell.setCellValue("BM25 Similarity");
			headerCell.setCellStyle(headerStyle);
			
			FileOutputStream outputStream = new FileOutputStream(pathname+filename); 			
			workbook.write(outputStream);
			workbook.close();
						
			return true;
		}
		catch(Exception e){
			return false;
		}	
			
	}
	
	// Add AppReviews to existing file with specific template
	public boolean AppendFile(String pathname, String filename, List<Review> AppReviews) throws IOException{
		
		try{
			
			FileInputStream file = new FileInputStream(new File(pathname+filename));
			Workbook workbook = new XSSFWorkbook(file);
			Sheet sheet = workbook.getSheet("Results");
	
			CellStyle style = workbook.createCellStyle();
			style.setWrapText(true);
			
			int InitalRow = 0;
	
			// Each row in file correspond to single informative sentence in each review
			for(Review itr : AppReviews) {
				
				Row row = sheet.createRow(++InitalRow);
	
				// App Id
				Cell cell = row.createCell(0);
				cell.setCellValue(itr.getAppId());
				cell.setCellStyle(style);
				
				// Review Id
				cell = row.createCell(1);
				cell.setCellValue(itr.getReviewId());
				cell.setCellStyle(style);
				
				// Review Content
				cell = row.createCell(2);
				cell.setCellValue(itr.getContent());
				cell.setCellStyle(style);
						
				// OrginalQuery
				cell = row.createCell(3);
				cell.setCellValue(itr.getOrginalQuery());
				cell.setCellStyle(style);
				
				// ProcessedQuery
				cell = row.createCell(4);
				cell.setCellValue(itr.getProcessedQuery());
				cell.setCellStyle(style);
				
				// Similarity
				cell = row.createCell(5);
				cell.setCellValue(itr.getSimilarity());
				cell.setCellStyle(style);
			
			}
								 
			FileOutputStream outputStream = new FileOutputStream(pathname+filename); 			
			workbook.write(outputStream);
			workbook.close();
			
			return true;

		}catch(Exception e){

			System.out.print(e);
			return false;
		}

	}
	
}
