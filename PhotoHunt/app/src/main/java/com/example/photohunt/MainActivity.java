package com.example.photohunt;

import android.annotation.SuppressLint;

import android.app.AlertDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.graphics.Rect;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private ImageView originalImageView;
    private ImageView alteredImageView;
    private TextView scoreTextView;
    private Button buttonEasy, buttonMedium, buttonHard;
    private Bitmap originalBitmap, alteredBitmap;
    private List<Rect> detectedObjects;
    private int totalDifferences;
    private int attempts;
    private long startTime;
    private boolean gameActive;
    private String difficultyLevel = "easy";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        originalImageView = findViewById(R.id.originalImageView);
        alteredImageView = findViewById(R.id.alteredImageView);
        scoreTextView = findViewById(R.id.scoreTextView);
        buttonEasy = findViewById(R.id.buttonEasy);
        buttonMedium = findViewById(R.id.buttonMedium);
        buttonHard = findViewById(R.id.buttonHard);

        // Set listeners for difficulty buttons
        buttonEasy.setOnClickListener(view -> difficultyLevel = "easy");
        buttonMedium.setOnClickListener(view -> difficultyLevel = "medium");
        buttonHard.setOnClickListener(view -> difficultyLevel = "hard");

        // Set listener for selecting image
        findViewById(R.id.buttonSelectImage).setOnClickListener(view -> selectImageFromGallery());

        // Set listener for taking photo
        findViewById(R.id.buttonTakePhoto).setOnClickListener(view -> takePhoto());

        // Set touch listener for detecting differences
        alteredImageView.setOnTouchListener((view, motionEvent) -> {
            if (motionEvent.getAction() == MotionEvent.ACTION_DOWN) {
                Point tapPoint = new Point((int) motionEvent.getX(), (int) motionEvent.getY());
                onUserTap(tapPoint);
            }
            return true;
        });
    }

    private void selectImageFromGallery() {
        Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(intent, 1);
    }

    private void takePhoto() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(intent, 2);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && data != null) {
            Uri imageUri = data.getData();
            try {
                originalBitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), imageUri);
                alteredBitmap = originalBitmap.copy(Bitmap.Config.ARGB_8888, true);
                originalImageView.setImageBitmap(originalBitmap);
                alteredImageView.setImageBitmap(alteredBitmap);
                startGame();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void startGame() {
        detectedObjects = detectObjects(alteredBitmap);
        detectedObjects = filterObjectsByDifficulty(detectedObjects);
        alterImage(alteredBitmap, detectedObjects);
        totalDifferences = detectedObjects.size();
        attempts = 0;
        startTime = System.currentTimeMillis();
        gameActive = true;
        updateScoreText();
    }

    private List<Rect> detectObjects(Bitmap bitmap) {
        List<Rect> rectangles = new ArrayList<>();
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();
        int threshold = 50;

        for (int x = 0; x < width; x += threshold) {
            for (int y = 0; y < height; y += threshold) {
                int pixel = bitmap.getPixel(x, y);
                if (pixel != Color.WHITE) {  // Example check for non-white pixels (replace with a more complex check as needed)
                    Rect rect = new Rect(x, y, x + threshold, y + threshold);
                    rectangles.add(rect);
                }
            }
        }
        return rectangles;
    }

    private List<Rect> filterObjectsByDifficulty(List<Rect> detectedObjects) {
        List<Rect> filteredObjects = new ArrayList<>();
        for (Rect rect : detectedObjects) {
            switch (difficultyLevel) {
                case "easy":
                    if (rect.width() * rect.height() > 10000) { // Large objects
                        filteredObjects.add(rect);
                    }
                    break;
                case "medium":
                    if (rect.width() * rect.height() > 5000 && rect.width() * rect.height() <= 10000) { // Medium objects
                        filteredObjects.add(rect);
                    }
                    break;
                case "hard":
                    if (rect.width() * rect.height() <= 5000) { // Small objects
                        filteredObjects.add(rect);
                    }
                    break;
            }
        }
        return filteredObjects;
    }

    private void alterImage(Bitmap bitmap, List<Rect> objectsToHide) {
        Canvas canvas = new Canvas(bitmap);
        Paint paint = new Paint();
        paint.setColor(Color.WHITE);
        paint.setStyle(Paint.Style.FILL);

        for (Rect rect : objectsToHide) {
            canvas.drawRect(rect, paint);
        }

        alteredImageView.setImageBitmap(bitmap);
    }

    private void onUserTap(Point tapPoint) {
        if (!gameActive) return;

        attempts++;
        boolean foundDifference = false;

        for (Rect rect : detectedObjects) {
            if (rect.contains(tapPoint.x, tapPoint.y)) {
                foundDifference = true;
                detectedObjects.remove(rect);
                totalDifferences--;
                updateScoreText();
                break;
            }
        }

        if (totalDifferences == 0) {
            gameActive = false;
            long elapsedTime = System.currentTimeMillis() - startTime;
            showGameEndDialog(elapsedTime);
        } else if (!foundDifference) {
            Toast.makeText(this, "Try again!", Toast.LENGTH_SHORT).show();
        }
    }

    private void updateScoreText() {
        scoreTextView.setText("Differences left: " + totalDifferences + " | Attempts: " + attempts);
    }

    private void showGameEndDialog(long elapsedTime) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Game Over")
                .setMessage("Congratulations! You found all differences in " + elapsedTime / 1000 + " seconds with " + attempts + " attempts.")
                .setPositiveButton("OK", (dialog, which) -> dialog.dismiss())
                .show();
    }
}
